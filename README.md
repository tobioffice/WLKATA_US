# WLKATA_US - Automated Biscuit Quality Control System

An intelligent computer vision system for automated biscuit detection and quality assessment using OpenCV and Python. This system captures images of biscuits, detects their presence, analyzes their properties, and determines quality based on baking/burned state classification.

## 🎥 Demonstration Video

[![WLKATA_US Demo](https://i.ytimg.com/vi/7D_TxVvmXgU/hqdefault.jpg)](https://youtu.be/7D_TxVvmXgU)

**🎬 Watch the system in action**: [https://youtu.be/7D_TxVvmXgU](https://youtu.be/7D_TxVvmXgU)

See real-time biscuit detection, quality assessment, and automated sorting in our comprehensive demonstration video!

## 🚀 Features

- **Real-time Biscuit Detection**: Detects presence of biscuits using advanced computer vision techniques
- **Quality Assessment**: Analyzes area, angle, and baking state of detected biscuits
- **Multi-state Classification**: Classifies biscuits into 4 baking states (unBaked, underBaked, good, overBaked)
- **Serial Communication**: Interfaces with hardware for automated biscuit processing
- **Image Processing Pipeline**: Complete workflow from capture to quality decision

## 📁 Project Structure

```
WLKATA_US/
├── main.py                     # Main execution script
├── pyproject.toml             # Project dependencies
├── rgbMap.json               # RGB reference values for baking states
├── images/                   # Image storage directory
│   ├── no_object.png         # Background reference image (empty conveyor)
│   ├── pra*.png             # Sample/processed biscuit images
│   └── burnedStates/        # Reference images for each baking state
│       ├── good.png         # Perfectly baked biscuits
│       ├── overBurned.png   # Over-baked/burnt biscuits
│       ├── unBurned.png     # Under-baked/raw biscuits
│       └── underBurned.png  # Slightly under-baked biscuits
└── utils/                   # Core utility modules
    ├── captureImages.py     # Image capture and preprocessing
    ├── checkObject.py       # Biscuit detection algorithms
    ├── getBurnedState.py    # Baking state classification
    ├── checkAreaAndAngle.py # Geometric property analysis
    └── pickBadAndPlace.py   # Hardware control for biscuit handling
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- OpenCV
- NumPy
- PySerial
- UV (Python package manager)

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd WLKATA_US
```

2. Install dependencies using UV:

```bash
uv sync
```

3. Ensure your camera is connected (default: camera index 2)

4. Connect serial device to `/dev/ttyUSB0` (or update the port in `main.py`)

## 🎯 Usage

### Basic Execution

Run the main quality control loop:

```bash
uv run main.py
```

### Individual Module Testing

#### Test Object Detection

```bash
uv run utils/checkObject.py
```

#### Test Burned State Classification

```bash
uv run utils/getBurnedState.py
```

#### Test Image Capture

```bash
uv run utils/captureImages.py
```

## 🔍 How It Works

### 1. Image Capture (`captureImages.py`)

- Captures images from connected camera
- Performs preprocessing (cropping, grayscale conversion, binary thresholding)
- Saves processed images for analysis

### 2. Object Detection (`checkObject.py`)

Uses multiple detection methods for robust biscuit identification:

- **Difference Detection**: Compares current image with background
- **Edge Detection**: Uses Canny edge detection for dark objects
- **Adaptive Thresholding**: Handles local variations in lighting
- **Statistical Analysis**: Compares image properties (mean, std deviation)

**Key Parameters:**

- `CHANGE_THRESHOLD = 20`: Sensitivity for difference detection
- `MIN_OBJECT_AREA = 300`: Minimum area for valid biscuit detection
- `EDGE_THRESHOLD = 50`: Threshold for edge-based detection

### 3. Baking State Classification (`getBurnedState.py`)

Classifies biscuits into four baking states based on RGB color analysis:

- **unBaked**: Light grayish colors `(R>125, G>125, B>120)` - Raw/unbaked dough
- **underBaked**: Yellow/bright tones `(high R,G, low B)` - Slightly underbaked
- **good**: Orange/brown tones `(R>G>B with specific ratios)` - Perfectly baked
- **overBaked**: Dark colors `(R<90, G<90, B<90)` - Burnt/overbaked

**RGB Reference Values** (from `rgbMap.json`):

```json
{
  "unBurned": [
    [254, 255, 254],
    [253, 255, 252],
    [254, 255, 254]
  ],
  "underBurned": [
    [254, 238, 86],
    [254, 236, 92],
    [255, 255, 97]
  ],
  "overBurned": [
    [26, 27, 26],
    [107, 103, 98],
    [60, 60, 59]
  ],
  "good": [
    [254, 148, 61],
    [255, 181, 80],
    [255, 136, 48]
  ]
}
```

### 4. Quality Assessment Workflow

```python
# Main processing loop (simplified)
while attempt <= max_attempts:
    processImagesAndSave()           # Capture and preprocess
    objectDetected = idObjectPresent()  # Detect object presence

    if objectDetected:
        areaAngleGood = isAreaAndAngleGood()     # Check geometry
        if areaAngleGood:
            goodBurnedState = check_burned_state()  # Check quality
            badFound = not goodBurnedState
        else:
            badFound = True
    else:
        badFound = False

    pickBadAndPlace(badFound)        # Handle based on quality
```

## � Biscuit Baking State Examples

| State             | Description          | RGB Characteristics        |
| ----------------- | -------------------- | -------------------------- |
| **Good** ✅       | Perfect baking state | Orange/brown tones (R>G>B) |
| **UnBaked** ⚪    | Raw/unbaked dough    | Light grayish colors       |
| **UnderBaked** 🟡 | Slightly underbaked  | Yellow/bright tones        |
| **OverBaked** ⚫  | Burnt/overbaked      | Very dark colors           |

## ⚙️ Configuration

### Adjusting Detection Sensitivity

Edit `utils/checkObject.py`:

```python
CHANGE_THRESHOLD = 20    # Lower = more sensitive
MIN_OBJECT_AREA = 300    # Minimum pixels for detection
EDGE_THRESHOLD = 50      # Edge detection sensitivity
```

### Customizing Baking State Classification

Edit `utils/getBurnedState.py`:

```python
# Adjust color range thresholds
if r > 125 and g > 125 and b > 120:  # unBaked threshold
    predicted_state = "unBaked"
```

### Hardware Configuration

Edit `main.py`:

```python
serial_port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)  # Serial port
tryNO = 20  # Maximum attempts per session
```

## 🧪 Testing

### Test All Components

```bash
# Test biscuit detection with different baking states
python3 -c "
import sys; sys.path.append('./utils')
from checkObject import idObjectPresent
print('Background:', idObjectPresent('images/no_object.png'))
print('Good:', idObjectPresent('images/burnedStates/good.png'))
print('Overbaked:', idObjectPresent('images/burnedStates/overBurned.png'))
"
```

### Test Baking State Classification

```bash
# Test classification accuracy
uv run utils/getBurnedState.py
```

## 🔧 Troubleshooting

### Common Issues

1. **Camera not detected**

   - Check camera connection
   - Verify camera index in `captureImages.py` (default: 2)

2. **Serial port errors**

   - Ensure device is connected to `/dev/ttyUSB0`
   - Check permissions: `sudo chmod 666 /dev/ttyUSB0`

3. **Object detection too sensitive**

   - Increase `CHANGE_THRESHOLD` in `checkObject.py`
   - Increase `MIN_OBJECT_AREA` for larger biscuits only

4. **Baking state misclassification**
   - Check lighting conditions
   - Adjust color thresholds in `getBurnedState.py`
   - Verify RGB reference values in `rgbMap.json`

## 📊 Performance Metrics

The system provides detailed analysis output:

- Biscuit detection confidence
- Color analysis scores for each baking state
- Geometric property measurements
- Processing time per image

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with various biscuit types and baking states
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Python scientific computing ecosystem
- Contributors to the image processing algorithms

---

For questions or support, please open an issue in the repository.
