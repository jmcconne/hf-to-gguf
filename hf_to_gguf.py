import argparse
import json
from huggingface_hub import snapshot_download
import os

# Create the parser
parser = argparse.ArgumentParser(description='Process config.json file.')

# Add the arguments
parser.add_argument('ConfigFile', metavar='config', type=str, help='the config file with model_id')

# Parse the arguments
args = parser.parse_args()

# Load the JSON config file
with open(args.ConfigFile) as json_file:
    data = json.load(json_file)

# Extract the arguments
model_id = data["download"]["model_id"]
model_revision = data["download"]["model_revision"]
hf_to_gguf_version = data["conversion"]["hf_to_gguf_version"]
model_name_prefix = data["conversion"]["model_name_prefix"]
outtype = data["conversion"]["outtype"]
quant = data["quantization"]

# Checkout specific version of the script. If not specified, the latest version will be used.
if hf_to_gguf_version:
    os.system("git checkout " + hf_to_gguf_version)
else:
    hf_to_gguf_version = os.popen("git rev-parse --short HEAD").read().strip()
    os.system("git checkout " + hf_to_gguf_version)

# Define the downloads directory path
downloads_dir_path = "models/downloads/"

# Check if the downloads directory already exists
if not os.path.exists(downloads_dir_path):
    # If not, create the directory
    os.makedirs(downloads_dir_path)

username, repo_name = model_id.split("/")
snapshot_download(repo_id=model_id, local_dir=downloads_dir_path + username + "/" + repo_name,
                  local_dir_use_symlinks=True, revision=model_revision)

# Define the conversions directory path
conversions_dir_path = "models/conversions/" + username + "/" + repo_name + "/"

# Check if the conversions directory already exists
if not os.path.exists(conversions_dir_path):
    # If not, create the directory
    os.makedirs(conversions_dir_path)

# Execute Python script to convert the model
os.system("python llama.cpp/convert.py " + downloads_dir_path + username + "/" + repo_name + " --outfile " + conversions_dir_path + model_name_prefix + "." + outtype + ".gguf" + " --outtype " + outtype)

# Define the quantizations directory path
quantizations_dir_path = "models/quantizations/" + username + "/" + repo_name + "/"

# Check if the quantizations directory already exists
if not os.path.exists(quantizations_dir_path):
    # If not, create the directory
    os.makedirs(quantizations_dir_path)

# Execute script to quantize the model
os.system("llama.cpp/quantize " + conversions_dir_path + model_name_prefix + "." + outtype + ".gguf " + quantizations_dir_path + model_name_prefix + "." + quant + ".gguf " + quant)

# Create a JSON file with model information
config = {
    "download": {
        "model_id": model_id,
        "model_revision": model_revision
    },
    "conversion": {
        "hf_to_gguf_version": hf_to_gguf_version,
        "model_name_prefix": model_name_prefix,
        "outtype": outtype
    },
    "quantization": quant
}

with open(quantizations_dir_path + model_name_prefix + "." + quant + ".gguf" + ".config.json", "w") as json_file:
    json.dump(config, json_file, indent=4)
