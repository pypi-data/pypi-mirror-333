import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, PreTrainedModel
from tqdm.auto import tqdm
import numpy as np
from typing import List, Optional, Union, Dict, Any, Tuple
from pathlib import Path
import matplotlib.pyplot as plt
from torch.optim import AdamW
from torch.optim.lr_scheduler import LinearLR, CosineAnnealingLR, SequentialLR
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from collections import Counter
from adjustText import adjust_text

def set_device(device: Optional[str] = None) -> str:
    """
    Determine the appropriate device for computation.
    
    Args:
        device: Optional device specification ('cuda', 'mps', 'cpu', or None)
                If None, will return 'cpu'. Only returns 'cuda' or 'mps' if explicitly specified.
    
    Returns:
        str: The selected device ('cuda', 'mps', or 'cpu')
    """
    if device == "cuda":
        if torch.cuda.is_available():
            return "cuda"
        else:
            print("CUDA not available, using CPU")
            return "cpu"
    elif device == "mps":
        if torch.backends.mps.is_available():
            return "mps"
        else:
            print("MPS not available, using CPU")
            return "cpu"
    return "cpu"

class TextDataset(Dataset):
    def __init__(self, texts: List[str], 
                 tokenizer: AutoTokenizer, 
                 max_length: Optional[int] = None, 
                 labels: Optional[List[int]] = None):

        if labels is not None and len(labels) != len(texts):
            raise ValueError(f"Number of labels ({len(labels)}) must match number of texts ({len(texts)})")
            
        self.encodings = tokenizer(texts, 
                                   truncation=True, 
                                   padding=True,
                                   max_length=max_length,
                                   return_tensors='pt', 
                                   return_token_type_ids=False)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        if self.labels is not None:
            item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.encodings['input_ids'])

def plot_training_curves(
    history: Dict[str, Any],
    save_path: Path,
    title: str = 'Training Loss per Batch',
) -> None:
    """
    Plot training curves and save to file.
    
    Args:
        history: Dictionary containing training history
        save_path: Path to save the plot
        title: Title for the plot
    """
    plt.figure(figsize=(10, 5))
    
    # Plot batch losses
    batch_numbers, losses = zip(*history['batch_losses'])
    plt.plot(batch_numbers, losses, label='Training Loss')
    
    # Plot validation loss if available
    if history['val_loss'] is not None and len(history['val_loss']) > 0:
        # Create x-axis points for validation loss
        # Assuming validation happens once per epoch
        val_points = np.linspace(0, len(batch_numbers), len(history['val_loss']))
        plt.plot(val_points, history['val_loss'], 'r-', label='Validation Loss')
    
    plt.title(title)
    plt.xlabel('Batch Number')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def train_bert_classifier(
    model: AutoModelForSequenceClassification,
    train_dataset: Dataset,
    valid_dataset: Optional[Dataset] = None,
    batch_size: int = 16,
    learning_rate: float = 2e-5,
    num_epochs: int = 1,
    device: Optional[str] = None,
    scheduler_type: str = "linear",
    warmup_steps: int = 0,
    max_train_batches: Optional[int] = None,
    logging_dir: Optional[str] = None,
    save_dir: Optional[str] = None,
    plot_interval: int = 100,  # Plot every N batches
) -> Dict[str, Any]:
    """
    Train a BERT-based classifier with custom training loop.
    
    Args:
        model: Pre-loaded BERT model for classification
        train_dataset: PyTorch Dataset for training
        valid_dataset: Optional PyTorch Dataset for validation. If None, no validation is performed.
        batch_size: Training batch size
        learning_rate: Learning rate for training
        num_epochs: Number of training epochs
        device: Device to train on ('cuda', 'mps', or 'cpu')
        scheduler_type: Type of learning rate scheduler ('linear' or 'cosine')
        warmup_steps: Number of warmup steps for learning rate scheduler
        max_train_batches: Maximum number of training batches per epoch (for quick experiments)
        logging_dir: Directory to save training logs
        save_dir: Directory to save model checkpoints
        plot_interval: Number of batches between plot updates
    
    Returns:
        Dictionary containing training history and final model
    """
    print(f"Training set size: {len(train_dataset)}")
    if valid_dataset is not None:
        print(f"Validation set size: {len(valid_dataset)}")
    
    # Set device
    device = set_device(device)
    
    # Move model to device
    model = model.to(device)
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(valid_dataset, batch_size=batch_size) if valid_dataset is not None else None
    
    # Initialize optimizer
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    
    # Calculate total steps for scheduling
    total_steps = len(train_loader) * num_epochs
    if max_train_batches is not None:
        total_steps = min(max_train_batches, total_steps)
    
    if warmup_steps >= total_steps:
        raise ValueError(f"warmup_steps ({warmup_steps}) must be less than total_steps ({total_steps})")
    
    # Create warmup scheduler
    if warmup_steps > 0:
        warmup_scheduler = LinearLR(
            optimizer,
            start_factor=1e-6,
            end_factor=1.0,
            total_iters=warmup_steps
        )
        
        # Create main scheduler
        if scheduler_type == "linear":
            main_scheduler = LinearLR(
                optimizer,
                start_factor=1.0,
                end_factor=1e-6,
                total_iters=total_steps - warmup_steps
            )
        elif scheduler_type == "cosine":
            main_scheduler = CosineAnnealingLR(
                optimizer,
                T_max=total_steps - warmup_steps
            )
        else:
            raise ValueError(f"Unsupported scheduler type: {scheduler_type}")
        
        # Combine schedulers
        scheduler = SequentialLR(
            optimizer,
            schedulers=[warmup_scheduler, main_scheduler],
            milestones=[warmup_steps]
        )
    else:
        # No warmup, just use the main scheduler
        if scheduler_type == "linear":
            scheduler = LinearLR(
                optimizer,
                start_factor=1.0,
                end_factor=1e-6,
                total_iters=total_steps
            )
        elif scheduler_type == "cosine":
            scheduler = CosineAnnealingLR(
                optimizer,
                T_max=total_steps
            )
        else:
            raise ValueError(f"Unsupported scheduler type: {scheduler_type}")
    
    # Training history
    history = {
        'batch_losses': [],  # List of (batch_number, loss) tuples
        'val_loss': [] if valid_dataset is not None else None
    }
    
    # Setup logging directory
    if logging_dir:
        log_path = Path(logging_dir)
        log_path.mkdir(parents=True, exist_ok=True)
    
    # Training loop
    batch_number = 0
    finished_trainig = False

    for epoch in range(num_epochs):
        if finished_trainig:
            break
        model.train()
        total_loss = 0
        num_batches = 0
        
        progress_bar = tqdm(train_loader, desc=f'Epoch {epoch + 1}/{num_epochs}')
        
        for batch_idx, batch in enumerate(progress_bar):
            # Check if we've reached max_train_batches
            if max_train_batches is not None and batch_idx >= max_train_batches:
                finished_trainig = True
                break
                
            # Move batch to device
            batch = {k: v.to(device) for k, v in batch.items()}
            
            # Forward pass
            outputs = model(**batch)
            loss = outputs.loss
            
            # Backward pass
            loss.backward()
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
            
            # Get loss value and clear memory
            current_loss = loss.item()
            del outputs, loss
            if device == "cuda":
                torch.cuda.empty_cache()
            
            # Update metrics
            total_loss += current_loss
            num_batches += 1
            
            # Record batch loss
            history['batch_losses'].append((batch_number, current_loss))
            batch_number += 1
            
            # Update progress bar with current loss
            progress_bar.set_postfix({
                'loss': f'{current_loss:.4f}'
            })
            
            # Periodically update plots and save history
            if logging_dir and batch_number % plot_interval == 0:
                # Save history as JSON
                with open(log_path / 'training_history.json', 'w') as f:
                    json.dump(history, f)
                
                # Update plot
                plot_training_curves(
                    history=history,
                    save_path=log_path / 'training_curves.png',
                    title=f'Training Loss per Batch (Batch {batch_number})'
                )
        
        # Calculate epoch metrics
        epoch_loss = total_loss / num_batches
        
        print(f'Epoch {epoch + 1}:')
        print(f'Train Loss: {epoch_loss:.4f}')
        
        # Validation if val_dataset is provided
        if valid_dataset is not None:
            model.eval()
            val_loss = 0
            val_batches = 0
            
            with torch.no_grad():
                val_progress = tqdm(val_loader, desc=f'Validation')
                for batch in val_progress:
                    batch = {k: v.to(device) for k, v in batch.items()}
                    outputs = model(**batch)
                    current_val_loss = outputs.loss.item()
                    val_loss += current_val_loss
                    val_batches += 1
                    val_progress.set_postfix({
                        'loss': f'{current_val_loss:.4f}'
                    })
                    
                    # Clear memory
                    del outputs
                    if device == "cuda":
                        torch.cuda.empty_cache()
            
            val_loss = val_loss / val_batches
            history['val_loss'].append(val_loss)
            
            print(f'Val Loss: {val_loss:.4f}')
        
        # Save checkpoint if save_dir is provided
        if save_dir:
            save_path = Path(save_dir) / f'checkpoint_epoch_{epoch+1}'
            save_path.mkdir(parents=True, exist_ok=True)
            model.save_pretrained(save_path)
    
    # Final plot and save if logging_dir is provided
    if logging_dir:
        # Save final history as JSON
        with open(log_path / 'training_history.json', 'w') as f:
            json.dump(history, f)
        
        # Create final plot
        plot_training_curves(
            history=history,
            save_path=log_path / 'training_curves.png',
            title=f'Training Loss per Batch (Final, Batch {batch_number})'
        )
    
    return {
        'model': model,
        'history': history,
        'train_size': len(train_dataset),
        'val_size': len(valid_dataset) if valid_dataset is not None else None
    }


def evaluate(
    model: AutoModelForSequenceClassification,
    dataset: Dataset,
    batch_size: int = 32,
    device: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Evaluate a BERT-based classifier on a dataset.
    
    Args:
        model: Pre-loaded BERT model for classification
        dataset: PyTorch Dataset to evaluate
        batch_size: Batch size for evaluation
        device: Device to evaluate on ('cuda', 'mps', or 'cpu')
    
    Returns:
        Dictionary containing evaluation metrics and statistics
    """
    # Input validation
    if len(dataset) == 0:
        raise ValueError("Dataset is empty")
    
    # Set device
    device = set_device(device)
    
    # Move model to device
    model = model.to(device)
    model.eval()
    
    # Create dataloader
    dataloader = DataLoader(dataset, batch_size=batch_size)
    
    # Process batches
    all_labels = []
    all_predictions = []
    
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating"):
            # Get labels
            labels = batch['labels'].numpy()
            all_labels.extend(labels)
            
            # Move batch to device
            batch = {k: v.to(device) for k, v in batch.items()}
            
            # Forward pass
            outputs = model(**batch)
            
            # Get predictions
            predictions = torch.argmax(outputs.logits, dim=-1)
            all_predictions.extend(predictions.cpu().numpy())
            
            # Clear GPU memory if needed
            if device == "cuda":
                torch.cuda.empty_cache()
    
    # Convert to numpy arrays
    all_labels = np.array(all_labels)
    all_predictions = np.array(all_predictions)
    
    # Sanity check: verify number of unique labels matches model's num_labels
    unique_labels = np.unique(all_labels)
    if len(unique_labels) != model.config.num_labels:
        raise ValueError(
            f"Number of unique labels ({len(unique_labels)}) does not match "
            f"model's expected number of labels ({model.config.num_labels})"
        )
    
    # Calculate metrics with different averaging methods
    accuracy = accuracy_score(all_labels, all_predictions)
    
    # Weighted average (takes class imbalance into account)
    weighted_precision, weighted_recall, weighted_f1, _ = precision_recall_fscore_support(
        all_labels, 
        all_predictions, 
        average='weighted'
    )
    
    # Macro average (treats all classes equally)
    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
        all_labels, 
        all_predictions, 
        average='macro'
    )
    
    # Calculate per-class metrics
    class_metrics = {}
    for label in unique_labels:
        class_precision, class_recall, class_f1, _ = precision_recall_fscore_support(
            all_labels == label,
            all_predictions == label,
            average='binary'
        )
        class_metrics[f'class_{label}'] = {
            'precision': class_precision,
            'recall': class_recall,
            'f1': class_f1,
            'support': np.sum(all_labels == label)
        }
    
    # Calculate confusion matrix
    conf_matrix = confusion_matrix(all_labels, all_predictions)
    
    # Create results dictionary
    results = {
        'accuracy': accuracy,
        'weighted_avg': {
            'precision': weighted_precision,
            'recall': weighted_recall,
            'f1': weighted_f1
        },
        'macro_avg': {
            'precision': macro_precision,
            'recall': macro_recall,
            'f1': macro_f1
        },
        'class_metrics': class_metrics,
        'confusion_matrix': conf_matrix.tolist(),
        'predictions': all_predictions.tolist(),
        'true_labels': all_labels.tolist()
    }
    
    # Print summary
    print("\nEvaluation Results:")
    print(f"Accuracy: {accuracy:.4f}")
    
    print("\nWeighted Average (accounts for class imbalance):")
    print(f"Precision: {weighted_precision:.4f}")
    print(f"Recall: {weighted_recall:.4f}")
    print(f"F1 Score: {weighted_f1:.4f}")
    
    print("\nMacro Average (treats all classes equally):")
    print(f"Precision: {macro_precision:.4f}")
    print(f"Recall: {macro_recall:.4f}")
    print(f"F1 Score: {macro_f1:.4f}")
    
    print("\nPer-class Metrics:")
    for label, metrics in class_metrics.items():
        print(f"\n{label}:")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1: {metrics['f1']:.4f}")
        print(f"  Support: {metrics['support']}")
    
    print("\nConfusion Matrix:")
    print(conf_matrix)
    
    return results

def predict(
    model: AutoModelForSequenceClassification,
    texts: Optional[List[str]] = None,
    dataset: Optional[Dataset] = None,
    tokenizer: Optional[AutoTokenizer] = None,
    batch_size: int = 32,
    device: Optional[str] = None,
    return_probs: bool = False,
) -> Union[List[int], Dict[str, Any]]:
    """
    Make predictions on new texts using a trained BERT classifier.
    
    Args:
        model: Pre-loaded BERT model for classification
        texts: List of texts to predict (required if dataset is None)
        dataset: PyTorch Dataset to use for inference (required if texts is None)
        tokenizer: Pre-loaded tokenizer corresponding to the model (required if texts is provided)
        batch_size: Batch size for inference
        device: Device to run inference on ('cuda', 'mps', or 'cpu')
        return_probs: Whether to return prediction probabilities
    
    Returns:
        If return_probs is False:
            List of predicted labels
        Otherwise:
            Dictionary containing:
                - 'labels': List of predicted labels
                - 'probabilities': List of probability distributions
    """
    # Validate input arguments
    if texts is None and dataset is None:
        raise ValueError("Either texts or dataset must be provided")
    if texts is not None and dataset is not None:
        raise ValueError("Cannot provide both texts and dataset")
    if texts is not None and tokenizer is None:
        raise ValueError("tokenizer must be provided when using texts")
    
    # Set device
    device = set_device(device)
    
    # Move model to device and set to eval mode
    model = model.to(device)
    model.eval()
    
    # Create dataloader
    if texts is not None:
        # Create dataset from texts
        dataset = TextDataset(texts, tokenizer)
    
    dataloader = DataLoader(dataset, batch_size=batch_size)
    
    # Initialize results
    all_predictions = []
    all_probabilities = [] if return_probs else None
    
    # Inference loop
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Classifying"):
            # Move batch to device
            batch = {k: v.to(device) for k, v in batch.items()}
            
            # Forward pass
            outputs = model(**batch)
            
            # Get predictions and probabilities
            predictions = torch.argmax(outputs.logits, dim=-1)
            all_predictions.extend(predictions.cpu().numpy())
            
            if return_probs:
                probs = torch.softmax(outputs.logits, dim=-1)
                all_probabilities.extend(probs.cpu().numpy())
    
    # Convert numpy arrays to lists
    all_predictions = [int(x) for x in all_predictions]
    if return_probs:
        all_probabilities = [x.tolist() for x in all_probabilities]
    
    # Return results
    if return_probs:
        return {
            'predictions': all_predictions,
            'probabilities': all_probabilities
        }
    else:
        return all_predictions

def make_datasets(
    data: List[Tuple[str, int]],
    tokenizer: AutoTokenizer,
    split: Union[Tuple[float, float], Tuple[float, float, float]],
    max_length: Optional[int] = None,
    random_seed: int = 42,
) -> Union[Tuple[Dataset, Dataset], Tuple[Dataset, Dataset, Dataset]]:
    """
    Create train/val/test datasets from a list of (text, label) tuples with stratification.
    
    Args:
        data: List of tuples where each tuple contains (text, label)
        tokenizer: Tokenizer to use for text encoding
        split: Tuple of proportions for splits:
            - (train_prop, val_prop) for train/val split
            - (train_prop, val_prop, test_prop) for train/val/test split
        max_length: Maximum sequence length for tokenization
        random_seed: Random seed for reproducible splits
    
    Returns:
        If split has length 2:
            Tuple of (train_dataset, val_dataset)
        If split has length 3:
            Tuple of (train_dataset, val_dataset, test_dataset)
    """
    if len(split) not in [2, 3]:
        raise ValueError("split must be a tuple of length 2 or 3")
    
    if not all(0 < p < 1 for p in split):
        raise ValueError("All proportions must be between 0 and 1")
    
    if abs(sum(split) - 1.0) > 1e-6:
        raise ValueError("Proportions must sum to 1.0")
    
    # Unzip the data into texts and labels
    texts, labels = zip(*data)
    
    # Calculate split sizes
    total_size = len(texts)
    if len(split) == 2:
        train_prop, val_prop = split
        train_size = int(total_size * train_prop)
        val_size = total_size - train_size
        test_size = 0
    else:
        train_prop, val_prop, test_prop = split
        train_size = int(total_size * train_prop)
        val_size = int(total_size * val_prop)
        test_size = total_size - train_size - val_size
    
    # Create train/val split
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels,
        test_size=val_size + test_size,
        random_state=random_seed,
        stratify=labels
    )
    
    # Create test split if needed
    if len(split) == 3:
        # Further split validation data into val and test
        val_texts, test_texts, val_labels, test_labels = train_test_split(
            val_texts, val_labels,
            test_size=test_size,
            random_state=random_seed,
            stratify=val_labels
        )
    
    # Create datasets
    train_dataset = TextDataset(train_texts, tokenizer, max_length, train_labels)
    val_dataset = TextDataset(val_texts, tokenizer, max_length, val_labels)
    
    # Print split sizes
    print(f"Total samples: {total_size}")
    print(f"Training set size: {len(train_dataset)}")
    print(f"Validation set size: {len(val_dataset)}")
    
    if len(split) == 3:
        test_dataset = TextDataset(test_texts, tokenizer, max_length, test_labels)
        print(f"Test set size: {len(test_dataset)}")
        return train_dataset, val_dataset, test_dataset
    else:
        return train_dataset, val_dataset

def bert_encode(
    model: AutoModelForSequenceClassification,
    tokenizer: AutoTokenizer,
    texts: List[str],
    batch_size: Optional[int] = None,
    max_length: Optional[int] = None,
    pooling_strategy: str = 'cls',
    device: Optional[str] = None,
) -> List[np.ndarray]:
    """
    Extract embeddings from a transformer model for given text(s).
    
    Args:
        model: Pre-loaded transformer model (e.g., BERT, RoBERTa, etc.)
        tokenizer: Pre-loaded tokenizer corresponding to the model
        texts: List of texts to encode
        batch_size: If None, process texts individually. If provided, process in batches
        max_length: Maximum sequence length for tokenization
        pooling_strategy: Strategy for pooling embeddings ('cls' or 'mean')
        device: Device to run inference on ('cuda', 'mps', or 'cpu')
    
    Returns:
        List of numpy arrays, each of shape (hidden_size,)
        
    Raises:
        ValueError: If texts list is empty or pooling_strategy is invalid
    """
    # Input validation
    if not texts:
        raise ValueError("Texts list cannot be empty")
    if pooling_strategy not in ['cls', 'mean']:
        raise ValueError("pooling_strategy must be either 'cls' or 'mean'")
    
    # Set device
    device = set_device(device)
    
    # Move model to device and set to eval mode
    model = model.to(device)
    model.eval()
    
    # If max_length is not provided, use model's max length
    if max_length is None:
        max_length = getattr(model.config, 'max_position_embeddings', 512)
    
    # Process texts
    all_embeddings = []
    
    if batch_size is None:
        # Process one text at a time
        for text in tqdm(texts, desc="Processing texts"):
            # Tokenize single text
            inputs = tokenizer(
                text,
                truncation=True,
                max_length=max_length,
                padding=True,
                return_tensors='pt',
                return_token_type_ids=False
            )
            
            # Move inputs to device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Forward pass
            with torch.no_grad():
                outputs = model(**inputs)
                last_hidden_state = outputs.last_hidden_state
                attention_mask = inputs['attention_mask']
                
                # Apply pooling strategy
                if pooling_strategy == 'cls':
                    embeddings = last_hidden_state[:, 0, :]
                else:  # mean pooling
                    attention_mask = attention_mask.unsqueeze(-1)
                    sum_embeddings = torch.sum(last_hidden_state * attention_mask, dim=1)
                    sum_mask = torch.clamp(attention_mask.sum(dim=1), min=1e-9)
                    embeddings = sum_embeddings / sum_mask
                
                # Convert to numpy and add to list
                embeddings = embeddings.cpu().numpy()
                all_embeddings.append(embeddings[0])  # Remove batch dimension
                
                # Clear memory
                del outputs
                if device == "cuda":
                    torch.cuda.empty_cache()
    
    else:
        # Process in batches
        dataset = TextDataset(texts, tokenizer, max_length)
        dataloader = DataLoader(dataset, batch_size=batch_size)
        
        with torch.no_grad():
            for batch in tqdm(dataloader, desc="Processing batches"):
                # Move batch to device
                batch = {k: v.to(device) for k, v in batch.items()}
                
                # Forward pass
                outputs = model(**batch)
                last_hidden_state = outputs.last_hidden_state
                attention_mask = batch['attention_mask']
                
                # Apply pooling strategy
                if pooling_strategy == 'cls':
                    embeddings = last_hidden_state[:, 0, :]
                else:  # mean pooling
                    attention_mask = attention_mask.unsqueeze(-1)
                    sum_embeddings = torch.sum(last_hidden_state * attention_mask, dim=1)
                    sum_mask = torch.clamp(attention_mask.sum(dim=1), min=1e-9)
                    embeddings = sum_embeddings / sum_mask
                
                # Convert to numpy and add to list
                embeddings = embeddings.cpu().numpy()
                all_embeddings.extend(embeddings)
                
                # Clear memory
                del outputs
                if device == "cuda":
                    torch.cuda.empty_cache()
    
    return all_embeddings

def add_corpus_tags(corpora, labels, target_words):
    """
    Add corpus-specific tags to target words in all corpora at once.
    
    Args:
        corpora: List of corpora (each corpus is list of tokenized sentences)
        labels: List of corpus labels
        target_words: List of words to tag
    
    Returns:
        List of processed corpora where target words have been tagged with their corpus label
    """
    processed_corpora = []
    target_words_set = set(target_words)
    
    for corpus, label in zip(corpora, labels):
        processed_corpus = []
        for sentence in corpus:
            processed_sentence = []
            for token in sentence:
                if token in target_words_set:
                    processed_sentence.append(f"{token}_{label}")
                else:
                    processed_sentence.append(token)
            processed_corpus.append(processed_sentence)
        processed_corpora.append(processed_corpus)
    
    return processed_corpora

def semantic_change(corpora_data, target_words, method='consecutive', min_freq=5, top_n=None, 
                   stopwords=None, window=5, min_length=1, vector_size=256, epochs=5, 
                   anchor_words=1000, limit_most_similar=None, return_models=False):
    """
    Analyze semantic change of target words across consecutive corpora using either independent
    or consecutive training approach.
    
    Args:
        corpora_data: List of (label, corpus) tuples, where each corpus is a list of tokenized sentences
                     The order of tuples determines the order of analysis
        target_words: List of words to track for semantic change
        method: Analysis method ('consecutive' or 'independent')
                - consecutive: Train one model with tagged words
                - independent: Train separate models and align with Procrustes
        min_freq: Minimum frequency threshold for words
        top_n: Number of top similar/dissimilar words to return (if None, return all)
        stopwords: Set of stopwords to exclude from final results
        window: Context window size for Word2Vec
        min_length: Minimum length of words to include in analysis
        vector_size: Size of word vectors
        epochs: Number of training epochs
        anchor_words: Number of most frequent words to use for alignment (default=1000)
        limit_most_similar: If provided, only include words that are among the N most
                          similar words to the target in either time period
        return_models: Whether to return trained Word2Vec models along with results
    
    Returns:
        If return_models=False:
            Dict of format:
            {
                'corpus1->corpus2': {
                    'target_word1': [(word1, change1), (word2, change2), ...],
                    'target_word2': [(word1, change1), (word2, change2), ...]
                },
                ...
            }
        If return_models=True:
            Tuple (results_dict, models_dict)
    """
    # Extract labels and corpora from the input tuples, maintaining order
    labels = [label for label, _ in corpora_data]
    corpora = [corpus for _, corpus in corpora_data]
    transformations = None
    
    if method == 'consecutive':
        results, models = _semantic_change_consecutive(
            corpora, labels, target_words, min_freq, top_n,
            stopwords, window, min_length, vector_size, epochs,
            limit_most_similar
        )
    elif method == 'independent':
        results, models, transformations = _semantic_change_independent(
            corpora, labels, target_words, min_freq, top_n,
            stopwords, window, min_length, vector_size, epochs,
            anchor_words, limit_most_similar
        )
    else:
        raise ValueError("Method must be 'consecutive' or 'independent'")
    
    if return_models:
        return results, models, transformations
    return results

def _semantic_change_consecutive(corpora, labels, target_words, min_freq=5, top_n=None,
                           stopwords=None, window=5, min_length=1, vector_size=256, 
                           epochs=5, limit_most_similar=None):
    """
    Analyze semantic change using consecutive training approach.
    Internal helper function for semantic_change().
    """
    from gensim.models import Word2Vec
    from sklearn.metrics.pairwise import cosine_similarity
    from tqdm.auto import tqdm
    import numpy as np
    import random
    from collections import Counter
    random.seed(42)
    
    results = {}
    models = {}
    
    # Process all corpora to add tags to target words
    processed_corpora = add_corpus_tags(corpora, labels, target_words)
    
    # Create list of consecutive pairs for the progress bar
    corpus_pairs = list(zip(labels[:-1], labels[1:]))
    
    # Analyze each consecutive pair of corpora
    pbar = tqdm(enumerate(corpus_pairs), total=len(corpus_pairs), 
               desc="Analyzing corpus pairs (consecutive)")
    for i, (label1, label2) in pbar:
        label_pair = f"{label1}->{label2}"
        pbar.set_description(f"Analyzing: {label1}->{label2}")
        
        # Count tokens in both corpora using Counter
        tokens_prev = sum(len(sent) for sent in processed_corpora[i])
        tokens_next = sum(len(sent) for sent in processed_corpora[i+1])
        min_tokens = min(tokens_prev, tokens_next)
        
        # Sample sentences to match token count
        def sample_sentences_to_token_count(corpus, target_tokens):
            sampled_sentences = []
            current_tokens = 0
            sentence_indices = list(range(len(corpus)))
            random.shuffle(sentence_indices)
            
            for idx in sentence_indices:
                sentence = corpus[idx]
                if current_tokens + len(sentence) <= target_tokens:
                    sampled_sentences.append(sentence)
                    current_tokens += len(sentence)
                if current_tokens >= target_tokens:
                    break
            return sampled_sentences
        
        corpus_prev = sample_sentences_to_token_count(processed_corpora[i], min_tokens)
        corpus_next = sample_sentences_to_token_count(processed_corpora[i+1], min_tokens)
        combined_corpus = corpus_prev + corpus_next
        
        # Train Word2Vec model on combined corpus
        model = Word2Vec(sentences=combined_corpus,
                       vector_size=vector_size,
                       window=window,
                       min_count=min_freq,
                       workers=1,
                       epochs=epochs,
                       seed=42)
        
        models[label_pair] = model
        
        # Get vocabulary that appears in both corpora with minimum frequency using Counter
        vocab_counts_prev = Counter(word for sent in corpus_prev for word in sent)
        vocab_counts_next = Counter(word for sent in corpus_next for word in sent)
        
        # Find common vocabulary meeting frequency requirements (without min_length filter)
        common_vocab = [word for word in vocab_counts_prev if 
                      word in vocab_counts_next and
                      vocab_counts_prev[word] >= min_freq and
                      vocab_counts_next[word] >= min_freq and
                      word in model.wv.key_to_index]
        
        # Get vectors for all common words
        vocab_vectors = np.array([model.wv[word] for word in common_vocab])
        results[label_pair] = {}
        
        # Analyze each target word
        for target in target_words:
            target_prev = f"{target}_{labels[i]}"
            target_next = f"{target}_{labels[i+1]}"
            
            if target_prev not in model.wv or target_next not in model.wv:
                continue
            
            # If limit_most_similar is provided, filter common_vocab to only include
            # words that are among the most similar to either target state
            if limit_most_similar is not None:
                similar_prev = set(word for word, _ in model.wv.most_similar(target_prev, topn=limit_most_similar))
                similar_next = set(word for word, _ in model.wv.most_similar(target_next, topn=limit_most_similar))
                similar_words = similar_prev.union(similar_next)
                
                # Filter common_vocab and vocab_vectors
                filtered_indices = [i for i, word in enumerate(common_vocab) if word in similar_words]
                if not filtered_indices:  # Skip if no similar words found
                    continue
                    
                filtered_vocab = [common_vocab[i] for i in filtered_indices]
                filtered_vectors = vocab_vectors[filtered_indices]
                
                # Update for the rest of the analysis
                common_vocab = filtered_vocab
                vocab_vectors = filtered_vectors
            
            sims_prev = cosine_similarity(
                model.wv[target_prev].reshape(1, -1),
                vocab_vectors
            )[0]
            
            sims_next = cosine_similarity(
                model.wv[target_next].reshape(1, -1),
                vocab_vectors
            )[0]
            
            changes = [(word, sim_next - sim_prev) 
                      for word, sim_prev, sim_next 
                      in zip(common_vocab, sims_prev, sims_next)]
            
            # Filter results by min_length and stopwords (keeping corpus tags intact)
            filtered_changes = []
            for word, change in changes:
                if len(word) >= min_length and (not stopwords or word not in stopwords):
                    filtered_changes.append((word, change))
            
            filtered_changes.sort(key=lambda x: x[1], reverse=True)
            
            if top_n is not None:
                moved_towards = filtered_changes[:top_n]
                moved_away_from = filtered_changes[-top_n:]
                filtered_changes = moved_towards + moved_away_from
            
            results[label_pair][target] = filtered_changes
    
    return results, models

def _semantic_change_independent(corpora, labels, target_words, min_freq=5, top_n=None,
                             stopwords=None, window=5, min_length=1, vector_size=256, 
                             epochs=5, anchor_words=1000, limit_most_similar=None):
    """
    Analyze semantic change using independent training approach with Procrustes alignment.
    Internal helper function for semantic_change().
    """
    from gensim.models import Word2Vec
    from sklearn.metrics.pairwise import cosine_similarity
    from tqdm.auto import tqdm
    import numpy as np
    from collections import Counter
    
    results = {}
    models = {}
    transformations = {}  # Store transformation matrices for each transition
    
    # Train separate models for each corpus and count words
    word_counts = []  # Store word counts for each corpus
    corpus_sizes = []  # Store total words in each corpus
    pbar = tqdm(enumerate(corpora), total=len(corpora), 
               desc="Training individual models")
    
    for i, corpus in pbar:
        pbar.set_description(f"Training model for corpus: {labels[i]}")
        
        # Count word frequencies using Counter
        counts = Counter(word for sent in corpus for word in sent)
        total_words = sum(counts.values())
        word_counts.append(counts)
        corpus_sizes.append(total_words)
        
        model = Word2Vec(sentences=corpus,
                       vector_size=vector_size,
                       window=window,
                       min_count=min_freq,
                       workers=1,
                       epochs=epochs,
                       seed=42)
        models[labels[i]] = model
    
    # Analyze consecutive pairs
    corpus_pairs = list(zip(labels[:-1], labels[1:]))
    pbar = tqdm(enumerate(corpus_pairs), 
               total=len(corpus_pairs), desc="Analyzing model pairs (independent)")
    
    for i, (label1, label2) in pbar:
        model1 = models[label1]
        model2 = models[label2]
        label_pair = f"{label1}->{label2}"
        pbar.set_description(f"Analyzing: {label1}->{label2}")
        
        # Get word counts and corpus sizes
        counts1 = word_counts[i]
        counts2 = word_counts[i+1]
        size1 = corpus_sizes[i]
        size2 = corpus_sizes[i+1]
        
        # Find common vocabulary between models (excluding target words)
        common_vocab = [word for word in model1.wv.key_to_index 
                      if word in model2.wv.key_to_index and
                      counts1[word] >= min_freq and
                      counts2[word] >= min_freq and
                      word not in target_words]
        
        # Calculate relative frequencies and select anchor words
        # Note: We use ALL frequent words (including stopwords) for alignment
        rel_freqs = {}
        for word in common_vocab:
            freq1 = counts1[word] / size1
            freq2 = counts2[word] / size2
            # Use geometric mean of relative frequencies as stability measure
            rel_freqs[word] = (freq1 * freq2) ** 0.5
        
        # Sort by frequency and select top anchor_words
        anchor_vocab = sorted(rel_freqs.items(), key=lambda x: x[1], reverse=True)
        anchor_vocab = [word for word, _ in anchor_vocab[:anchor_words]]
        
        if len(anchor_vocab) < 2:
            print(f"Not enough anchor words found for {label1}->{label2}")
            anchor_vocab = common_vocab  # Fallback to all common words if not enough anchors
        
        # Get vectors for alignment using anchor words
        anchor_vecs1 = np.array([model1.wv[word] for word in anchor_vocab])
        anchor_vecs2 = np.array([model2.wv[word] for word in anchor_vocab])
        
        # Align second space to first space using anchor words
        _, transformation = align_vectors(anchor_vecs2, anchor_vecs1)
        transformations[label_pair] = transformation  # Store the transformation matrix
        
        # Get vectors for all common words (for similarity computation)
        vecs1 = np.array([model1.wv[word] for word in common_vocab])
        
        results[label_pair] = {}
        
        # Analyze each target word
        for target in target_words:
            if target not in model1.wv or target not in model2.wv:
                continue
            
            # If limit_most_similar is provided, filter common_vocab
            if limit_most_similar is not None:
                similar1 = set(word for word, _ in model1.wv.most_similar(target, topn=limit_most_similar))
                similar2 = set(word for word, _ in model2.wv.most_similar(target, topn=limit_most_similar))
                similar_words = similar1.union(similar2)
                
                # Filter common_vocab and vectors
                filtered_indices = [i for i, word in enumerate(common_vocab) if word in similar_words]
                if not filtered_indices:  # Skip if no similar words found
                    continue
                    
                filtered_vocab = [common_vocab[i] for i in filtered_indices]
                filtered_vecs = vecs1[filtered_indices]
                
                # Update for the rest of the analysis
                common_vocab = filtered_vocab
                vecs1 = filtered_vecs
            
            # Get target vectors from both spaces
            target_vec1 = model1.wv[target]
            target_vec2 = model2.wv[target]
            
            # Align target vector from second space using the same transformation
            aligned_target_vec2 = np.dot(target_vec2.reshape(1, -1), transformation.T)
            
            # Calculate similarities with common vocabulary
            sims1 = cosine_similarity(
                target_vec1.reshape(1, -1),
                vecs1
            )[0]
            
            sims2 = cosine_similarity(
                aligned_target_vec2,
                vecs1
            )[0]
            
            changes = [(word, sim2 - sim1) 
                      for word, sim1, sim2 
                      in zip(common_vocab, sims1, sims2)]
            
            # Filter results by min_length and stopwords
            filtered_changes = []
            for word, change in changes:
                if len(word) >= min_length and (not stopwords or word not in stopwords):
                    filtered_changes.append((word, change))
            
            filtered_changes.sort(key=lambda x: x[1], reverse=True)
            
            if top_n is not None:
                moved_towards = filtered_changes[:top_n]
                moved_away_from = filtered_changes[-top_n:]
                filtered_changes = moved_towards + moved_away_from
            
            results[label_pair][target] = filtered_changes
    
    return results, models, transformations

def align_vectors(source_vectors, target_vectors):
    """
    Align source vectors with target vectors using Procrustes analysis.
    
    Args:
        source_vectors: numpy array of vectors to be aligned
        target_vectors: numpy array of vectors to align to
        
    Returns:
        Tuple of (aligned_vectors, transformation_matrix)
        - aligned_vectors: The aligned source vectors
        - transformation_matrix: The orthogonal transformation matrix that can be used to align other vectors
    """
    # Center the vectors
    source_centered = source_vectors - np.mean(source_vectors, axis=0)
    target_centered = target_vectors - np.mean(target_vectors, axis=0)
    
    # Compute the covariance matrix
    covariance = np.dot(target_centered.T, source_centered)
    
    # Compute SVD
    U, _, Vt = np.linalg.svd(covariance)
    
    # Compute the rotation matrix
    rotation = np.dot(U, Vt)
    
    # Apply the rotation to the source vectors
    aligned_vectors = np.dot(source_vectors, rotation.T)
    
    return aligned_vectors, rotation

def visualize_semantic_trajectory(semantic_change_results, target_word, word2vec_models, 
                                method='pca', n_neighbors=5, perplexity=30, figsize=(12, 8),
                                filename=None, transformations=None, adjust_text_labels=False,
                                target_position_method='neighbor_mean'):
    """
    Visualize the semantic trajectory of a target word across corpora by showing its movement
    relative to its most significant neighbors in each transition period.
    
    Args:
        semantic_change_results: Results dictionary from semantic_change function
        target_word: The target word to visualize
        word2vec_models: Dictionary mapping corpus pairs to Word2Vec models (consecutive approach)
                       or corpus labels to models (independent approach)
        method: Dimensionality reduction method ('pca' or 'tsne')
        n_neighbors: Number of most significant neighbors to show for each transition
        perplexity: Perplexity parameter for t-SNE (if method='tsne')
        figsize: Figure size tuple
        filename: If provided, save the plot to this file
        transformations: Dictionary mapping corpus pairs to transformation matrices (independent approach)
        adjust_text_labels: Whether to use adjustText to prevent label overlap
        target_position_method: How to determine target word position ('embedding' or 'neighbor_mean')
                              'embedding': Project target word vector along with neighbor vectors
                              'neighbor_mean': Use mean of neighbor vectors (default)
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    
    if target_position_method not in ['embedding', 'neighbor_mean']:
        raise ValueError("target_position_method must be either 'embedding' or 'neighbor_mean'")
    
    # Get all corpus labels in order
    corpus_pairs = list(semantic_change_results.keys())

    # Determine if we're using consecutive or independent approach
    is_consecutive = transformations is None
    
    for idx, pair in enumerate(corpus_pairs):
        # Create a new figure for each transition
        plt.figure(figsize=figsize)
        label1, label2 = pair.split('->')
        
        # Get the appropriate model(s) based on approach
        if is_consecutive:
            model = word2vec_models[pair]
            target_prev = f"{target_word}_{label1}"
            target_next = f"{target_word}_{label2}"
            if target_prev not in model.wv or target_next not in model.wv:
                plt.text(0.5, 0.5, f"Word not found in {pair}", 
                       ha='center', va='center')
                plt.close()
                continue
        else:
            model1 = word2vec_models[label1]
            model2 = word2vec_models[label2]
            if target_word not in model1.wv or target_word not in model2.wv:
                plt.text(0.5, 0.5, f"Word not found in {pair}", 
                       ha='center', va='center')
                plt.close()
                continue
        
        # Get the most significant neighbors from semantic change results
        changes = semantic_change_results[pair][target_word]
        if not changes:
            plt.text(0.5, 0.5, f"No significant changes in {pair}", 
                   ha='center', va='center')
            plt.close()
            continue
        
        # Get top words moved towards and away from
        moved_towards = [word for word, change in changes[:n_neighbors] if change > 0]
        moved_away = [word for word, change in changes[-n_neighbors:] if change < 0]
        neighbor_words = moved_towards + moved_away
        
        # Get vectors for neighbor words and target words if using embedding method
        if is_consecutive:
            neighbor_vectors = np.array([model.wv[word] for word in neighbor_words])
            if target_position_method == 'embedding':
                all_vectors = np.vstack([
                    neighbor_vectors,
                    model.wv[target_prev].reshape(1, -1),
                    model.wv[target_next].reshape(1, -1)
                ])
            else:
                all_vectors = neighbor_vectors
        else:
            neighbor_vectors = np.array([model1.wv[word] for word in neighbor_words])
            if target_position_method == 'embedding':
                # For independent models, align vectors from second model
                target_vec1 = model1.wv[target_word].reshape(1, -1)
                target_vec2 = np.dot(model2.wv[target_word].reshape(1, -1), 
                                   transformations[pair].T)
                all_vectors = np.vstack([neighbor_vectors, target_vec1, target_vec2])
            else:
                all_vectors = neighbor_vectors
        
        # Project vectors to 2D
        if method == 'pca':
            projector = PCA(n_components=2)
            projected = projector.fit_transform(all_vectors)
            explained_var = projector.explained_variance_ratio_
            x_label = f"PC1 ({explained_var[0]:.1%} variance)"
            y_label = f"PC2 ({explained_var[1]:.1%} variance)"
        else:
            projector = TSNE(n_components=2, perplexity=perplexity)
            projected = projector.fit_transform(all_vectors)
            x_label = "Dimension 1"
            y_label = "Dimension 2"
        
        # Split projected points back into neighbors and targets
        if target_position_method == 'embedding':
            neighbor_points = projected[:-2]  # All but last two points are neighbors
            target_prev_point = projected[-2]  # Second-to-last point is target_prev
            target_next_point = projected[-1]  # Last point is target_next
        else:
            neighbor_points = projected
            n_towards = len(moved_towards)
            # Calculate centers of each group
            target_prev_point = np.mean(neighbor_points[n_towards:], axis=0)  # Away center
            target_next_point = np.mean(neighbor_points[:n_towards], axis=0)  # Towards center
        
        # Plot all neighbor words in the same color
        plt.scatter(neighbor_points[:, 0], neighbor_points[:, 1],
                   c='gray', alpha=0.6, label='Context Words')
        
        # Plot target word positions
        plt.scatter([target_prev_point[0], target_next_point[0]], 
                   [target_prev_point[1], target_next_point[1]],
                   c='blue', s=100, label='Target Word')
        
        # Add arrow showing movement
        arrow = FancyArrowPatch(
            target_prev_point, target_next_point,
            arrowstyle='-|>',
            color='blue',
            mutation_scale=15
        )
        plt.gca().add_patch(arrow)
        
        # Add labels with adjustText if enabled
        texts = []
        # Add labels for neighbors
        for i, word in enumerate(neighbor_words):
            texts.append(plt.text(neighbor_points[i, 0], neighbor_points[i, 1], word,
                                fontsize=10, alpha=0.7))
        
        # Add labels for target words with corpus tags
        if is_consecutive:
            prev_label = target_prev
            next_label = target_next
        else:
            prev_label = f"{target_word} ({label1})"
            next_label = f"{target_word} ({label2})"
            
        texts.append(plt.text(target_prev_point[0], target_prev_point[1], prev_label,
                            fontsize=12, fontweight='bold', c='red'))
        texts.append(plt.text(target_next_point[0], target_next_point[1], next_label,
                            fontsize=12, fontweight='bold', c='red'))
        
        if adjust_text_labels:
            from adjustText import adjust_text
            adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5))
        
        plt.title(f"Transition: {label1} → {label2}", fontsize=14, pad=10)
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=10)
        
        # Adjust tick label sizes
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        
        # Ensure tight layout
        plt.tight_layout()
        
        # Save the plot
        if filename:
            transition_filename = f"{filename}_{pair}.png"
            plt.savefig(transition_filename, dpi=300, bbox_inches='tight')
            print(f"Saved plot for transition {pair} to {transition_filename}")
        
        plt.close()

def visualize_semantic_trajectory_complete(semantic_change_results, target_word, word2vec_models, 
                                        method='pca', n_neighbors=5, perplexity=30, figsize=(15, 10),
                                        filename=None, transformations=None, adjust_text_labels=False,
                                        target_position_method='neighbor_mean'):
    """
    Create a comprehensive visualization of a target word's semantic trajectory across all transitions
    in a single plot.
    
    Args:
        semantic_change_results: Results dictionary from semantic_change function
        target_word: The target word to visualize
        word2vec_models: Dictionary mapping corpus pairs to Word2Vec models
        method: Dimensionality reduction method ('pca' or 'tsne')
        n_neighbors: Number of most significant neighbors to show for each transition
        perplexity: Perplexity parameter for t-SNE (if method='tsne')
        figsize: Figure size tuple
        filename: If provided, save the plot to this file
        transformations: Dictionary mapping corpus pairs to transformation matrices (independent approach)
        adjust_text_labels: Whether to use adjustText to prevent label overlap
        target_position_method: How to determine target word position ('embedding' or 'neighbor_mean')
                              'embedding': Project target word vector along with neighbor vectors
                              'neighbor_mean': Use mean of neighbor vectors (default)
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    from adjustText import adjust_text
    
    if target_position_method not in ['embedding', 'neighbor_mean']:
        raise ValueError("target_position_method must be either 'embedding' or 'neighbor_mean'")
    
    # Get all corpus labels in order
    corpus_pairs = list(semantic_change_results.keys())
    all_labels = [corpus_pairs[0].split('->')[0]] + [pair.split('->')[1] for pair in corpus_pairs]
    
    # Determine if we're using consecutive or independent approach
    is_consecutive = transformations is None
    
    # Collect all neighbor words and their vectors
    all_neighbor_words = []
    all_neighbor_vectors = []
    all_target_vectors = []  # Store target vectors for embedding method
    
    # Process first transition to get initial position
    first_pair = corpus_pairs[0]
    first_changes = semantic_change_results[first_pair][target_word]
    
    if not first_changes:
        print(f"No changes found for first transition {first_pair}")
        return
    
    # Get initial neighbors (moved away from) for first target position
    moved_away = [word for word, change in first_changes[-n_neighbors:] if change < 0]
    all_neighbor_words.extend(moved_away)
    
    # Get vectors for first set of neighbors and first target position
    if is_consecutive:
        model = word2vec_models[first_pair]
        vectors = [model.wv[word] for word in moved_away]
        if target_position_method == 'embedding':
            first_target = f"{target_word}_{all_labels[0]}"
            all_target_vectors.append(model.wv[first_target])
    else:
        first_model = word2vec_models[all_labels[0]]
        vectors = [first_model.wv[word] for word in moved_away]
        if target_position_method == 'embedding':
            all_target_vectors.append(first_model.wv[target_word])
    
    all_neighbor_vectors.extend(vectors)
    
    # Process all transitions to get "moved towards" neighbors and remaining target positions
    for i, pair in enumerate(corpus_pairs):
        changes = semantic_change_results[pair][target_word]
        moved_towards = [word for word, change in changes[:n_neighbors] if change > 0]
        all_neighbor_words.extend(moved_towards)
        
        if is_consecutive:
            model = word2vec_models[pair]
            vectors = [model.wv[word] for word in moved_towards]
            if target_position_method == 'embedding':
                next_target = f"{target_word}_{all_labels[i+1]}"
                all_target_vectors.append(model.wv[next_target])
        else:
            next_model = word2vec_models[all_labels[i+1]]
            vectors = [next_model.wv[word] for word in moved_towards]
            if target_position_method == 'embedding':
                # Align vector from next model to first model's space
                target_vec = next_model.wv[target_word]
                for j in range(i+1):  # Apply all transformations up to this point
                    pair_key = f"{all_labels[j]}->{all_labels[j+1]}"
                    target_vec = np.dot(target_vec, transformations[pair_key].T)
                all_target_vectors.append(target_vec)
        
        all_neighbor_vectors.extend(vectors)
    
    # Convert to numpy arrays
    all_neighbor_vectors = np.array(all_neighbor_vectors)
    if target_position_method == 'embedding':
        all_target_vectors = np.array(all_target_vectors)
        # Combine neighbor and target vectors for projection
        all_vectors = np.vstack([all_neighbor_vectors, all_target_vectors])
    else:
        all_vectors = all_neighbor_vectors
    
    # Project all vectors to 2D
    if method == 'pca':
        projector = PCA(n_components=2)
        projected = projector.fit_transform(all_vectors)
        explained_var = projector.explained_variance_ratio_
        x_label = f"PC1 ({explained_var[0]:.1%} variance)"
        y_label = f"PC2 ({explained_var[1]:.1%} variance)"
    else:
        projector = TSNE(n_components=2, perplexity=perplexity)
        projected = projector.fit_transform(all_vectors)
        x_label = "Dimension 1"
        y_label = "Dimension 2"
    
    # Create the plot
    plt.figure(figsize=figsize)
    
    # Split projected points back into neighbors and targets
    if target_position_method == 'embedding':
        neighbor_points = projected[:-len(all_labels)]
        target_positions = projected[-len(all_labels):]
    else:
        neighbor_points = projected
        # Calculate target positions using neighbor means
        target_positions = []
        current_idx = 0
        
        # First position (based on moved_away from first transition)
        first_center = np.mean(neighbor_points[current_idx:current_idx + len(moved_away)], axis=0)
        target_positions.append(first_center)
        current_idx += len(moved_away)
        
        # Subsequent positions (based on moved_towards for each transition)
        for pair in corpus_pairs:
            moved_towards = [word for word, change in semantic_change_results[pair][target_word][:n_neighbors] if change > 0]
            if moved_towards:
                center = np.mean(neighbor_points[current_idx:current_idx + len(moved_towards)], axis=0)
                target_positions.append(center)
                current_idx += len(moved_towards)
        target_positions = np.array(target_positions)
    
    # Plot all neighbor words
    plt.scatter(neighbor_points[:, 0], neighbor_points[:, 1],
               c='gray', alpha=0.6, label='Context Words')
    
    # Plot target positions and trajectory
    plt.scatter(target_positions[:, 0], target_positions[:, 1],
               c='blue', s=100, label='Target Word')
    
    # Add arrows between target positions
    for i in range(len(target_positions) - 1):
        arrow = FancyArrowPatch(
            target_positions[i], target_positions[i + 1],
            arrowstyle='-|>',
            color='blue',
            mutation_scale=25
        )
        plt.gca().add_patch(arrow)
    
    # Add labels
    texts = []
    
    # Add neighbor word labels
    for i, word in enumerate(all_neighbor_words):
        texts.append(plt.text(neighbor_points[i, 0], neighbor_points[i, 1], word,
                            fontsize=10, alpha=0.7))
    
    # Add target word labels with corpus tags
    for i, label in enumerate(all_labels):
        if is_consecutive:
            target_label = f"{target_word}_{label}"
        else:
            target_label = f"{target_word} ({label})"
        texts.append(plt.text(target_positions[i, 0], target_positions[i, 1],
                            target_label, fontsize=12, fontweight='bold', c='red'))
    
    if adjust_text_labels:
        adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5))
    
    plt.title(f"Semantic Trajectory of '{target_word}' Across All Periods", fontsize=14, pad=10)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    # Adjust tick label sizes
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    # Ensure tight layout
    plt.tight_layout()
    
    # Save the plot if filename provided
    if filename:
        plt.savefig(f"{filename}_complete.png", dpi=300, bbox_inches='tight')
        print(f"Saved complete trajectory plot to {filename}_complete.png")
    
    plt.close()