This document details the reconnaissance engine designed for the Residue Recon project. It focuses exclusively on the artificial intelligence and image validation logic utilized to identify unmanaged urban residuals.
Setup Requirements
Minimum Hardware and Software

    Operating System: Linux (Ubuntu 20.04+) or Windows Subsystem for Linux (WSL2).

    Python: Version 3.8 or higher.

    Memory: 4GB RAM.

    Storage: 500MB available for model weights and environment.

Recommended Hardware (Optimization)

    GPU: NVIDIA GTX 1650 or higher with 4GB VRAM for CUDA-accelerated performance.

    Compute Platform: CUDA 11.8+ for real-time inference.

Installation and Environment Setup

    Virtual Environment Initialization
    Create a clean environment to manage dependencies and avoid library conflicts.
    
    Bash
    python3 -m venv venv
    source venv/bin/activate

    Core Dependency Deployment
    Install the necessary libraries for object detection, image processing, and perceptual hashing.
    
    Bash
    pip install ultralytics torch torchvision torchaudio imagehash Pillow

    Weight Initialization
    Place the trained best.pt file in the project root directory.

Model Architecture and Performance
Object Detection Logic

    Model: YOLOv8n (Nano), selected for sub-100ms inference on GTX 1650 hardware.

    Classification: Specifically tuned for urban waste artifacts, including bottles, cups, and bowls.

    Validation Threshold: Only detections with a confidence score above 0.5 are verified to maintain report integrity.

Anti-Fraud Perceptual Hashing

The engine utilizes structural fingerprinting to prevent duplicate submissions.

    Algorithm: Perceptual Hashing (pHash) through the imagehash library.

    Fingerprint Density: Generates a 64-bit unique string based on image structure rather than pixel data, ensuring resilience against resizing or minor edits.

    Duplicate Detection: The system calculates the Hamming distance between hashes; a difference of 6 or less identifies a duplicate report.

Model Execution

Verify the model setup by running the internal validation suite directly.

Bash
python3 model_service.py

A successful test will confirm the following metrics:

    Status: Verified or Rejected.

    Confidence: Float score (e.g., 0.85).

    Fingerprint: Unique 64-bit hex string.

    Inference Time: Measured in milliseconds.
