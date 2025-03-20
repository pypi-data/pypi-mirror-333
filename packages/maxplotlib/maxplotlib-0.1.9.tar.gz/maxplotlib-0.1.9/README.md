# Maxplotlib

## Autovisualization API

Example

```bash
maxplotlib "Show the trigonometry of music"
```

![example maxplotlib image](https://github.com/user-attachments/assets/f0b05633-8c13-4cb4-9292-d2321e699092)


General:

```bash
maxplotlib prompt --output=optional_output_folder --server=server_ip
```

### Setup

Make sure a **server** with a known IP address is on (see **Server** if you are doing this yourself).

```bash
pip install maxplotlib
export MAXPLOTLIB_SERVER_IP=192.168....
```

### How does it work?

Maxplotlib supports multiple LLM providers to generate [`matplotlib`](https://github.com/matplotlib/matplotlib) python scripts which are executed to produce images for the API response:

- **OpenAI**
- **Anthropic**
- **MLX**: Uses Llama 3.1 (implemented in [`mlx_lm`](https://github.com/ml-explore/mlx-examples/blob/main/llms/README.md))

### Server

Turning on a **server** allows other people to use your machine as a compute engine for `maxplotlib` API calls.

To turn on a **server**, install the requirements:

```bash
pip install 'maxplotlib[server]'
```

Then, navigate to the `server` directory and run the launch script:

```bash
cd src/server
./run_server
```

Once the **server** is on, remote `maxplotlib` API calls to your IP address will run on your machine.

You can also set these parameters using environment variables:

```bash
# Set default model for OpenAI
export OPENAI_MODEL=gpt-4o-mini

# Set default model for Anthropic
export ANTHROPIC_MODEL=claude-3-7-sonnet-20250219

# Set default model for MLX
export MLX_MODEL=mlx-community/Meta-Llama-3.1-8B-Instruct-8bit
```
