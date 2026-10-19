# 🌱 AgriTrace-AI

### AI-Powered Animal Tracking and Behaviour Monitoring for Smart Agriculture

AgriTrace-AI is an AI-powered agricultural monitoring project that combines computer vision, animal tracking, and behavioural analysis to support intelligent farm monitoring.

The system includes animal detection, multi-object tracking, activity analysis, animal identity management, and a web-based interface. It aims to help monitor animal movements and identify potentially unusual behavioural patterns using video data.

## ✨ Features

* **Animal Detection:** Detects animals in farm video footage using a YOLO-based object detection model.
* **Animal Tracking:** Tracks animals across video frames.
* **Activity Analysis:** Includes modules for detecting and classifying animal activities.
* **Behavioural Analysis:** Supports behavioural baselines and deviation analysis.
* **Animal Identity Management:** Includes components for managing animal identities and associated records.
* **Event Logging:** Provides modules for recording events and maintaining animal-related information.
* **Web Interface:** Uses a Next.js frontend to present the application's functionality.
* **Video Demonstration:** Includes sample and processed farm videos for demonstration.

## 🛠️ Technology Stack

| Technology      | Purpose                                 |
| --------------- | --------------------------------------- |
| Python          | AI processing and backend logic         |
| YOLO            | Animal detection                        |
| ByteTrack       | Multi-object tracking                   |
| Computer Vision | Video and frame analysis                |
| Next.js         | Frontend framework                      |
| React           | User interface                          |
| TypeScript      | Frontend development                    |
| JSON            | Structured records and behavioural data |
| Git and GitHub  | Version control and collaboration       |

## 🏗️ System Workflow

```text
Farm Video Input
       ↓
Animal Detection
       ↓
Animal Tracking
       ↓
Activity Detection and Classification
       ↓
Behavioural Analysis
       ↓
Animal Records and Event Logging
       ↓
Web Interface
```

The workflow illustrates the intended processing stages. The actual execution sequence depends on how the individual modules are integrated.

## 📂 Project Structure

```text
AgriTrace-AI/
├── ai/                 # AI and computer vision modules
├── backend/            # Python backend
├── database/           # Database-related files
├── frontend/           # Next.js web application
├── videos/             # Sample and processed videos
├── runs/               # Generated detection and tracking outputs
├── yolo11n.pt          # YOLO model weights
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

Install the following:

* Python
* Node.js and npm
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/Sankeerthanadileep/AgriTrace-AI.git
```

### 2. Navigate to the Project

```bash
cd AgriTrace-AI
```

### 3. Set Up the Python Environment

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the Python dependencies required by the project. If a root-level `requirements.txt` file is available, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the dependencies required by the individual Python modules.

### 4. Start the Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install the Node.js dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the following address in your browser:

http://localhost:3000

### 5. Run the AI and Backend Components

The AI pipeline and Python backend may require separate configuration and dependencies.

Check the relevant Python scripts and their required input files before running them. The exact commands depend on the current implementation and integration of the modules.

## 🌍 Potential Applications

* Smart agriculture and farm monitoring
* Livestock movement tracking
* Animal activity observation
* Behavioural deviation analysis
* Computer vision research
* AI-assisted agricultural management

## 🔮 Future Improvements

* Improve animal detection and tracking accuracy.
* Integrate the AI pipeline, backend, and frontend into a unified application.
* Support real-time video monitoring.
* Improve animal identity consistency across video sequences.
* Evaluate behavioural analysis using suitable datasets.
* Add configurable alerts and monitoring dashboards.
* Improve system performance and data management.

## 🎓 Project Information

* **Project:** AgriTrace-AI
* **Domain:** Artificial Intelligence and Smart Agriculture
* **Focus:** Computer Vision, Animal Tracking, and Behavioural Analysis
* **Type:** Collaborative Software Project

## 🤝 Contributions

Suggestions and improvements are welcome. You can fork the repository, create a feature branch, and submit a pull request.

## 📄 License

A license has not yet been specified for this project.

---

**AgriTrace-AI — Towards Smarter and More Intelligent Farm Monitoring.** 🌱
