from fastapi import FastAPI, Form, Query
from fastapi.responses import JSONResponse
from time import time
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from maxplotlib.run import user_message_to_python_scripts, python_scripts_to_images

app = FastAPI(debug=False)

def validate_user_input(user_input: str, max_user_input_chars: int = 2000) -> str:
    if len(user_input) > max_user_input_chars:
        raise ValueError(f"Input is {len(user_input)} chars, maximum is {max_user_input_chars} characters.")
    return user_input
    
@app.post("/plot/")
async def plot_api(
    prompt: str = Form(...),
    provider: str = Form("openai"),
    model: Optional[str] = Form(None),
    temperature: float = Form(0.0),
    num_ideas: int = Form(4)
):
    """
    Generate matplotlib plots based on the user prompt.
    
    Args:
        prompt: The user's prompt describing the visualization
        provider: LLM provider to use ('mlx', 'openai', 'anthropic')
        model: Specific model to use (provider-dependent)
        temperature: Temperature for generation (0.0 = deterministic)
        num_ideas: Number of visualization ideas to generate
    """
    prompt = validate_user_input(prompt)
    
    # Configure provider-specific parameters
    provider_kwargs = {}
    
    if provider.lower() == "openai":
        # Use environment variable or specified model
        provider_kwargs["model"] = model or os.environ.get("OPENAI_MODEL", "gpt-4o")
    elif provider.lower() == "anthropic":
        # Use environment variable or specified model
        provider_kwargs["model"] = model or os.environ.get("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    elif provider.lower() == "mlx":
        # Use environment variable or default model
        provider_kwargs["model_name"] = model or os.environ.get("MLX_MODEL", "mlx-community/Meta-Llama-3.1-8B-Instruct-8bit")
    
    # Generate plots
    matplotlib_scripts, captions = user_message_to_python_scripts(
        prompt, 
        provider=provider,
        provider_kwargs=provider_kwargs,
        num_ideas=num_ideas,
        idea_temp=temperature,
        script_temp=temperature
    )
    
    images = python_scripts_to_images(matplotlib_scripts, captions)
    
    return JSONResponse(content={
        "timestamp": time(), 
        "prompt": prompt, 
        "provider": provider,
        "model": provider_kwargs.get("model") or provider_kwargs.get("model_name"),
        "python_scripts": matplotlib_scripts, 
        "images": images
    })