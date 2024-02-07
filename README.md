# hf-to-gguf

`hf-to-gguf` is a Python-based project that faciltates the quantization and conversion of LLMs residing in Hugging Face into the GGUF format. Quantized, GGUF formatted LLMs reside in a single file and provide for efficient inference on a broad range of hardware. Both conversion to GGUF and quantization are handled by Georgi Gerganov's [llama.cpp](https://github.com/ggerganov/llama.cpp), a submodule of this project. Though many LLMs are available on Hugging Face that have already been converted to GGUF and quantized, they often lack complete traceability and reproducibility. In addition to outputting quantized, GGUF formatted model files, `hf-to-gguf` will produce an accompanying JSON file containing the source and version of the model being convereted, version of conversion scripts, quantization method, and anything else needed to fully reproduce the converted model.

## Installation

1. Clone the project repository to your local machine:

   ```
   git clone https://github.com/jmcconne/hf-to-gguf.git
   ```

2. Create and activate Python virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install project dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Initialize, fetch and checkout nested submodules:

   ```
   git submodule update --init --recursive
   ```

5. Build llama.cpp:

    ```
    make -C llama.cpp
    ```
## Usage

1. Create a `config.json` file that specifies the source model on Hugging Face as well as the conversion and quantization paramaters. `config.json.example` can be used a template:

   ```
   {
       "download": {
           "model_id": "<model_repo>", # HF model repo to be downloaded
           "model_revision": "<commit_hash>" # Commit hash for HF model    version to be downloaded. Can be short or long commit hash.
       },
       "conversion": {
           "hf_to_gguf_version": "<commit_hash>", # Commit hash of    hf-to-gguf repo to be used for conversion. Can be short or long    commit hash. If left empty, latest commit will be used.
           "model_name_prefix": "<model_name_prefix>", # Model name prefix    to be used for converted model
           "outtype": "<output_type>" # Type to convert to. It is    recommended to retain the original model type and rely on    quantization to reduce the model size. Run "llama.cpp/convert.py    --help" for possible values.
       },
       "quantization": "<quant_type>" # Quantization type to be used. Run    "llama.cpp/quantize --help" for possible values.
   }
   ```

2. Download, convert, and quantize the model based on `config.json`:

   ```
   python3 hf_to_gguf.py config.json
   ```
   
   Downloaded files appear in `./models/downloads/`, converted models    appear in `./models/conversions/`, and the final converted and quantized models appear in `./models/quantizations/` along with the accompanying JSON files. Provided those JSON files are stored anywhere the model is deployed (e.g. locally, cloud server, Hugging Face, etc.), anyone can trace how that model was created and reproduce it if needed.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the project repository to your own GitHub account.
2. Clone the forked repository to your local machine.
3. Create a new branch for your changes.
4. Make your changes and commit them to your branch.
5. Push your branch to your forked repository.
6. Open a pull request to the original project repository.
