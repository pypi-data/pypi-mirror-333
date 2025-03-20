import { NotebookPanel } from '@jupyterlab/notebook';

// Function to detect GPU usage in code
export const detectGPUUsage = (code: string): boolean => {
  console.log('Checking for GPU usage in code...');
  
  // Pattern matching for common GPU usage in PyTorch
  const torchGPUPatterns = [
    /import torch/,
    /\.cuda\(\)/,
    /\.to\(['"]cuda['"]\)/,
    /\.to\(['"]mps['"]\)/, // Track an MPS for now too.
    /\.to\(device=['"]cuda['"]\)/,
    /torch\.cuda\./,
    /device\s*=\s*['"]cuda['"]/,
    /torch\.device\(['"]cuda['"]\)/
  ];
  
  // Pattern matching for TensorFlow GPU usage
  const tfGPUPatterns = [
    /import tensorflow/,
    /with tf\.device\(['"]\/GPU/,
    /tf\.config\.list_physical_devices\(['"]GPU['"]\)/
  ];
  
  // Pattern matching for JAX GPU usage
  const jaxGPUPatterns = [
    /import jax/,
    /jax\.device_put/,
    /jax\.devices\(\)/
  ];
  
  // Pattern matching for Hugging Face Transformers
  const transformersPatterns = [
    /from transformers import/,
    /Trainer\(/,
    /trainer\.train\(\)/,
    /training_args.*device/i,
    /TrainingArguments\(/
  ];
  
  // Check if any pattern matches
  const result = [...torchGPUPatterns, ...tfGPUPatterns, ...jaxGPUPatterns, ...transformersPatterns]
    .some(pattern => pattern.test(code));
  
  console.log({result, code})
  console.log(`GPU usage detection result: ${result ? 'GPU usage detected' : 'No GPU usage detected'}`);
  return result;
};

// Function to inject GPU monitoring code into the kernel
export const injectGPUMonitoring = async (notebook: NotebookPanel | null): Promise<void> => {
  if (!notebook) return;
  
  // Execute Python code in the kernel to set up monitoring
  const code = `
    import sys
    
    # Flag to track if GPU libraries are imported
    _gpu_libraries_imported = False
    
    # Original import function
    _original_import = __import__
    
    # Custom import hook to detect GPU libraries
    def _gpu_import_hook(name, *args, **kwargs):
        global _gpu_libraries_imported
        
        # Check for GPU-related libraries
        if name in ['torch', 'tensorflow', 'jax', 'cupy', 'transformers']:
            _gpu_libraries_imported = True
            
            # Additional checks for specific libraries
            if name == 'torch':
                # Check if CUDA is available
                exec('import torch; print("CUDA Available:", torch.cuda.is_available())')
            
            # Check for Hugging Face Transformers
            if name == 'transformers':
                try:
                    # Check if a GPU device is being used
                    exec('from transformers import TrainingArguments; print("Default device:", TrainingArguments(output_dir="./tmp").device)')
                except:
                    pass
            
        # Call the original import
        return _original_import(name, *args, **kwargs)
    
    # Replace the built-in import function
    sys.__import__ = _gpu_import_hook
    
    # Function to check GPU status
    def check_gpu_status():
        result = {"gpu_used": False, "memory_usage": 0, "library": None}
        
        if _gpu_libraries_imported:
            result["gpu_used"] = True
            
            # Try to get more detailed information based on available libraries
            try:
                import torch
                if torch.cuda.is_available():
                    result["library"] = "PyTorch"
                    result["memory_usage"] = torch.cuda.memory_allocated() / (1024**3)  # GB
            except:
                pass
                
            try:
                import tensorflow as tf
                gpus = tf.config.list_physical_devices('GPU')
                if gpus:
                    result["library"] = "TensorFlow"
                    # TF doesn't easily exposes memory usage
            except:
                pass
            
            try:
                import transformers
                result["library"] = "Transformers"
            except:
                pass
        
        return result
  `;
  
  // Execute this in the current notebook's kernel
  const session = notebook.sessionContext.session;
  await session?.kernel?.requestExecute({ code }).done;
}; 