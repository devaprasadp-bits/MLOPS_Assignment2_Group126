# 📦 Submission Guide - MLOps Assignment 2

## 1. GitHub Repository Checklist

### ✅ Files to COMMIT (Push to GitHub)

#### Source Code
```
✅ src/                          # All training and inference code
   ├── train.py                  # Model training with MLflow
   ├── inference.py              # FastAPI service
   ├── model.py                  # CNN architecture
   ├── data_preprocessing.py     # Data pipeline
   ├── monitoring.py             # Metrics tracking
   └── prepare_dataset.py        # Dataset splitting utility
✅ tests/                        # Test suite
   ├── test_preprocessing.py     # 10+ preprocessing tests
   ├── test_model.py             # 15+ model tests
   └── smoke_test.py             # Post-deployment tests
```

#### Configuration Files
```
✅ requirements.txt              # Pinned Python dependencies
✅ requirements-dev.txt          # Optional dev tools
✅ setup.cfg                     # Tool configurations (flake8, pytest, mypy)
✅ Dockerfile                    # Container definition  
✅ docker-compose.yml            # Multi-container setup (API + MLflow)
✅ .gitignore                    # Git ignore rules
✅ Makefile                      # Development commands
```

#### CI/CD Workflows
```
✅ .github/workflows/ci.yml      # Continuous Integration
✅ .github/workflows/cd.yml      # Continuous Deployment
```

#### Kubernetes Deployment
```
✅ deployment/kubernetes/
   └── deployment.yaml           # K8s manifests (Deployment + Service + Namespace)
```

#### Data Versioning
```
✅ .dvc/                         # DVC configuration
✅ data.dvc                      # DVC data tracking file
```

#### Documentation
```
✅ README.md                     # Project overview and setup instructions
```

### ❌ Files to EXCLUDE (Already in .gitignore)

```
❌ venv/                         # Virtual environment (too large, incompatible Python versions)
❌ __pycache__/                  # Python bytecode
❌ .pytest_cache/                # Test cache
❌ *.pyc                         # Compiled Python files
❌ .DS_Store                     # macOS system files
❌ data/                         # Raw dataset (1GB+, download from Kaggle)
❌ models/*.h5                   # Trained models (450MB+, regenerate with training)
❌ mlruns/                       # MLflow data (regenerated during training)
❌ .coverage                     # Coverage data files
❌ htmlcov/                      # HTML coverage reports
❌ coverage.xml                  # Coverage XML reports
❌ logs/                         # Log files  
❌ scripts/                      # Helper scripts (kept in repo for reviewers)
❌ examples/                     # Sample test files (kept in repo for reviewers)
❌ internal/                     # Internal docs (kept in repo, not for grading)
```

**Important Notes:**
- **Models excluded**: Trained model (cats_dogs_model.h5) is ~50MB and excluded from repo. Regenerate with: `python src/train.py --epochs 20`
- **Dataset excluded**: 1GB dataset must be downloaded from Kaggle. Instructions in README 
- **MLflow runs excluded**: Regenerated during training. All experiments will be tracked when you run training
- **Keep repo under 50MB**: Without models/data, repo should be lightweight for easy cloning
- **Document reproduction**: README has clear steps for evaluators to reproduce everything

### 📤 Delivery Format

**Recommended: GitHub + Video Link**
1. Push all code to GitHub repository
2. Create private/public video on YouTube/Loom
3. Submit:
   - GitHub repository URL
   - Video link
   - (Optional) README_SUBMISSION.txt with both links

**Alternative: Zip File**
```
Submission/
├── Source_Code/                 # All project files
│   ├── src/
│   ├── tests/
│   ├── .github/
│   ├── deployment/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── Video_Link.txt               # YouTube/Loom URL
└── GitHub_Link.txt              # Repository URL (if pushed)
```

**⚠️ Do NOT include in zip:**
- `venv/` folder (incompatible, too large)
- `data/` folder (1GB, download from Kaggle)
- `models/*.h5` files (large, regenerate with training)
- `mlruns/` folder (regenerated)
- `.git/` folder (if providing zip without GitHub)

---

## 2. GitHub Actions CI/CD Configuration

### Is GitHub Actions Required?

**Yes!** Module 3 (CI Pipeline) and Module 4 (CD Pipeline) explicitly require:
- Automated testing on code push
- Docker image build and registry push
- Automated deployment to Kubernetes
- Post-deployment smoke tests

### How to Activate GitHub Actions

#### Step 1: Verify Workflow Files Exist
```bash
# Check CI workflow
cat .github/workflows/ci.yml

# Check CD workflow  
cat .github/workflows/cd.yml
```

You should see:
- **ci.yml**: Test → Build → Publish (3 jobs)
- **cd.yml**: Deploy → Smoke-Test (2 jobs)

#### Step 2: Configure GitHub Secrets

GitHub Actions needs these secrets to run. Go to:
**Settings → Secrets and variables → Actions → New repository secret**

Required secrets:
```
DOCKER_USERNAME       # Your Docker Hub username
DOCKER_PASSWORD       # Docker Hub access token (NOT password!)
KUBE_CONFIG          # Base64-encoded ~/.kube/config
API_URL              # Deployed API URL for smoke tests
```

**Detailed instructions**: See `internal/GITHUB_SECRETS_SETUP.md`

#### Step 3: Push to GitHub

```bash
# Create repository on GitHub (via web interface)
# Name: MLOPS_Assignment2_Group126

# Then push:
git remote add origin https://github.com/YOUR_USERNAME/MLOPS_Assignment2_Group126.git
git branch -M main  
git push -u origin main
```

#### Step 4: Watch CI/CD Run

1. Go to GitHub repository
2. Click **Actions** tab
3. You'll see "CI Pipeline" workflow running automatically
4. After CI succeeds, "CD Pipeline" will trigger

### What the CI Pipeline Does

**Job 1: Test (runs on every push)**
- ✅ Checks out code
- ✅ Sets up Python 3.9
- ✅ Installs dependencies from requirements.txt
- ✅ Runs pytest with 25+ unit tests
- ✅ Generates coverage report
- ✅ Uploads coverage to Codecov

**Job 2: Build (after tests pass)**
- ✅ Creates dummy model file (for build testing)
- ✅ Builds Docker image with buildx
- ✅ Uses caching for faster builds
- ✅ Tags image with commit SHA

**Job 3: Publish (only on main branch)**
- ✅ Logs into Docker Hub
- ✅ Pushes image to Docker Hub
- ✅ Tags as both `latest` and SHA
- ✅ Makes image available for deployment

### What the CD Pipeline Does

**Job 1: Deploy (after successful CI)**
- ✅ Only runs if CI passed
- ✅ Sets up kubectl
- ✅ Configures Kubernetes access
- ✅ Updates deployment with new image
- ✅ Waits for rollout to complete (5min timeout)
- ✅ Verifies pods are running

**Job 2: Smoke Test (after deployment)**
- ✅ Installs test dependencies
- ✅ Runs smoke_test.py against deployed API
- ✅ Tests /health endpoint
- ✅ Tests /predict endpoint with sample image
- ✅ Fails pipeline if tests don't pass

### Quick Test of GitHub Actions

```bash
# Make a small change
echo "# Testing CI/CD" >> README.md

# Commit and push
git add README.md
git commit -m "test ci/cd pipeline"
git push

# Watch in GitHub Actions tab!
```

---

## 3. Video Demonstration Script (5 Minutes)

### 🎬 Complete Narration Script - 5 Minutes

**Recording Requirements:**
- **Duration**: **Under 5 minutes** (strict requirement!)
- **Content**: "Complete MLOps workflow from code change to deployed model prediction"
- **Format**: Screen recording with narration
- **Quality**: 1080p minimum, clear audio
- **Pace**: Faster than Assignment 1 - focus on flow, not details

**Pro Tip**: Practice twice before recording. 5 minutes goes fast!

---

#### **[0:00 - 0:20] Introduction & Project Overview**

*"Hello, I'm [Your Name] from Group 126, and this is our MLOps Assignment 2 demonstration.*

*We've built a complete end-to-end MLOps pipeline for Cats vs Dogs image classification, covering all five required modules: Model Development, Containerization, CI, CD, and Monitoring.*

*Let me walk you through the workflow from code change to live prediction in under 5 minutes."*

**On Screen:** Show terminal at project root

```bash
# Show project structure briefly
ls -la
```

**Pro Tip:** Don't dwell here - just a quick glance to orient viewers. You have 5 minutes total!

---

#### **[0:20 - 0:50] Module 1: Model Development & Experiment Tracking**

*"Module 1 covers model development and experiment tracking.*

*Our CNN model is defined in src/model.py - a 4-layer convolutional architecture.*

*The training script uses MLflow to track all experiments automatically."*

**On Screen:** Show code briefly

```bash
# Quick peek at model
head -30 src/model.py

# Show MLflow integration in train.py
grep -A 3 "mlflow.start_run" src/train.py
```

**Pro Tip:** Don't open full files - use `head` and `grep` for speed.

*"Let me start the MLflow UI to show experiment tracking."*

**Actions:**
```bash
# Start MLflow in background
mlflow ui --port 5000 &
sleep 2

# Open browser
open http://localhost:5000
```

**On Screen:** MLflow UI with experiments

*"Here's the MLflow interface showing all our training runs.*

*Each experiment logged metrics like accuracy, loss, precision, and recall.*

*The best model achieved around 90% test accuracy on the Cats vs Dogs dataset.*

*Click into any run to see parameters, metrics over time, and model artifacts."*

**Pro Tip:** Click into ONE experiment, show metrics panel, then move on. Don't explore every tab - 30 seconds max for MLflow!

*"For data versioning, we use DVC which tracks the 1GB dataset without storing it in Git."*

```bash
# Show DVC file
cat data.dvc
```

**Pro Tip:** Just flash the file - don't read it aloud.

---

#### **[0:50 - 1:30] Module 2: Containerization & API**

*"Module 2 packages everything into Docker containers.*

*Our FastAPI application has three endpoints: root info, health check, and prediction."*

**Actions:**
```bash
# Show Dockerfile
head -20 Dockerfile
```

**Pro Tip:** Scroll quickly - emphasize "multi-stage build" visually.

*"The Dockerfile uses a multi-stage build to keep the image around 1.2GB - which includes TensorFlow.*

*Let me start the API with docker-compose."*

**Actions:**
```bash
# Start services
docker-compose up -d

# Wait 3 seconds
sleep 3

# Show running containers
docker ps
```

**On Screen:** Show containers running

*"Docker Compose starts both the API on port 8000 and MLflow on port 5000.*

*Let me test the API endpoints."*

**Actions:**
```bash
# Health check
curl http://localhost:8000/health | jq

# Prediction with sample image (prepare this file beforehand!)
curl -X POST "http://localhost:8000/predict" \
  -F "file=@test_cat.jpg" | jq
```

**Pro Tip:** Have a small test image ready (test_cat.jpg) in project root BEFORE recording!

**On Screen:** Show JSON responses

*"The health endpoint confirms the service is up and the model is loaded.*

*The predict endpoint returns 'cat' with 95% confidence.*

*Notice we also get prediction time and a timestamp - important for production monitoring."*

**Pro Tip:** Speak while output appears - no dead air!

---

#### **[1:30 - 2:30] Module 3: CI Pipeline - Automated Testing**

*"Module 3 implements continuous integration with GitHub Actions.*

*Every code push triggers automated testing."*

**On Screen:** Open browser to GitHub repository

**Actions:**
```
# Navigate in browser:
1. Go to github.com/YOUR_USERNAME/MLOPS_Assignment2_Group126
2. Click "Actions" tab
3. Click on latest CI Pipeline run
```

**Pro Tip:** Have this pre-loaded in a browser tab before recording!

*"Here's the CI pipeline we configured in GitHub Actions.*

*The workflow has three stages: Test, Build, and Publish.*

*In the Test stage, pytest runs our 25+ unit tests covering preprocessing, model architecture, and API endpoints."*

**On Screen:** Click into test job, show test output

*"All tests passed with good coverage.*

*The Build stage creates a Docker image using the same Dockerfile we showed earlier.*

*And the Publish stage pushes that image to Docker Hub, but only on the main branch."*

**On Screen:** Show publish job (or Docker Hub)

*"You can see the image tagged with both 'latest' and the specific commit SHA for traceability."*

**Pro Tip:** If you can't show live CI run, show Docker Hub repository with images. Have this open in advance!

**Actions if showing tests locally:**
```bash
# Quickly show tests passing
pytest tests/ -v --tb=short
```

**Pro Tip:** Let it run for 5-10 seconds then Ctrl+C - you don't need full output in the video.

---

#### **[2:30 - 3:40] Module 4: CD Pipeline - Kubernetes Deployment**

*"Module 4 automates deployment to Kubernetes.*

*After CI succeeds, the CD pipeline deploys the new image automatically."*

**On Screen:** GitHub Actions - CD Pipeline

*"The CD workflow is triggered only after successful CI on the main branch.*

*It updates the Kubernetes deployment, waits for the rollout, and then runs automated smoke tests."*

**Pro Tip:** Flash the CD workflow YAML or GitHub Actions UI - don't narrate every line.

*"Let me show you the live Kubernetes deployment."*

**Actions:**
```bash
# Switch to terminal
kubectl get all -n mlops
```

**On Screen:** Show Kubernetes resources

*"Here's our deployment running in the 'mlops' namespace.*

*We have 2 pods running - both in READY state.*

*The deployment manages these replicas, and the LoadBalancer service exposes them."*

**Pro Tip:** Use your cursor to point at key parts: READY 2/2, STATUS Running, service type LoadBalancer.

*"Let me demonstrate Kubernetes' self-healing by deleting a pod."*

**Actions:**
```bash
# Get pod name
kubectl get pods -n mlops

# Delete one pod
kubectl delete pod cats-dogs-deployment-XXXXX-XXXXX -n mlops

# Watch briefly
kubectl get pods -n mlops -w
```

**On Screen:** Show pod terminating and new one creating

*"Watch - I deleted a pod, and Kubernetes immediately creates a replacement.*

*The new pod moves from Pending to Running within seconds.*

*This is automatic self-healing with no manual intervention."*

**Press Ctrl+C after 5-10 seconds**

*"Now let me scale the deployment."*

**Actions:**
```bash
# Scale to 5 replicas
kubectl scale deployment cats-dogs-deployment --replicas=5 -n mlops

# Show result
kubectl get pods -n mlops
```

**On Screen:** Show 5 pods

*"With one command, we scaled from 2 to 5 replicas.*

*In production, HorizontalPodAutoscaler would do this automatically based on CPU or request rate."*

**Pro Tip:** This entire K8s section should be 60-70 seconds max. Practice the timing!

*"Let me access the deployed API through Kubernetes."*

**Actions:**
```bash
# Get service URL (have minikube tunnel running beforehand!)
minikube service cats-dogs-service --url -n mlops

# Or if tunnel already running, just show the URL
echo "http://192.168.49.2:30080"  # Use your actual URL

# Test deployed API
curl http://YOUR-MINIKUBE-IP:PORT/health | jq
```

**On Screen:** Show health response from K8s deployment

*"Perfect - the API is live and responding through Kubernetes!"*

---

#### **[3:40 - 4:30] Module 5: Monitoring & Complete CI/CD Flow**

*"Module 5 implements monitoring and logging.*

*Our FastAPI application has structured logging throughout."*

**Actions:**
```bash
# Show logs from one pod
kubectl logs -n mlops deployment/cats-dogs-deployment --tail=15
```

**On Screen:** Show log entries

*"Every request is logged with timestamps, endpoints, and response times.*

*The monitoring module tracks prediction counts, confidence scores, and performance metrics."*

**Pro Tip:** Point out a log entry showing a prediction request - highlight the structure.

*"Now let me demonstrate the complete CI/CD workflow from code change to deployment."*

**Actions:**
```bash
# Make a small code change
echo "# CI/CD test" >> README.md

# Show the change
git diff README.md
```

**On Screen:** Show git diff

*"I've made a small change to the README.*

*Let me commit and push to trigger the CI/CD pipeline."*

**Actions:**
```bash
git add README.md
git commit -m "demonstrate cicd flow"
git push origin main
```

**On Screen:** Show git push output

*"The push triggers GitHub Actions automatically."*

**Switch to browser - GitHub Actions**

**On Screen:** Show CI Pipeline starting/running

*"Within seconds, GitHub Actions picks up the change.*

*The CI pipeline starts: it will run tests, build a new Docker image, and push to Docker Hub.*

*Once CI completes successfully, the CD pipeline will automatically deploy the new image to Kubernetes and run smoke tests."*

**Pro Tip:** You don't need to wait for it to finish - just show that it started. If you pre-recorded a successful run, show that instead!

*"The smoke tests validate the deployed API by calling the health and predict endpoints with a test image.*

*If any test fails, the deployment is marked as failed and can be rolled back."*

---

#### **[4:30 - 5:00] Wrap-up & Summary**

*"Let me quickly show the repository structure one more time."*

**Actions:**
```bash
tree -L 2 -I 'venv|__pycache__|.pytest_cache|mlruns|data'
```

**Pro Tip:** Have this command ready - tree output should be brief and clean.

**On Screen:** Show directory tree

*"To summarize what we've built:*

*Module 1: CNN model with MLflow experiment tracking and DVC data versioning.*

*Module 2: FastAPI REST API containerized with Docker, exposing health and prediction endpoints.*

*Module 3: CI pipeline with automated testing, Docker builds, and registry publishing.*

*Module 4: CD pipeline with Kubernetes deployment, self-healing, and scaling.*

*Module 5: Structured logging and monitoring throughout the application."*

*"The complete workflow goes from code commit to GitHub, through automated testing and building, to live deployment on Kubernetes - all without manual intervention.*

*The system is production-ready with testing, monitoring, and automated deployment.*

*Thank you for watching. The code is available at [show GitHub URL on screen]."*

**On Screen:** Final shot showing:
- GitHub repository URL
- Your name/group number
- "MLOps Assignment 2 - Group 126"

**Pro Tip:** End with a clean slate - no error messages, terminal should show a successful state.

---

## 4. Recording Setup & Pro Tips

### Before You Start Recording

#### Environment Setup
```bash
# 1. Clean everything
docker-compose down
docker system prune -f
kubectl delete namespace mlops --ignore-not-found
minikube delete
clear

# 2. Start fresh
minikube start
mlflow ui --port 5000 &
docker-compose up -d

# 3. Wait for everything to be ready
sleep 10

# 4. Load image to minikube (IMPORTANT!)
minikube image load cats-dogs-classifier:latest

# 5. Deploy to Kubernetes
kubectl apply -f deployment/kubernetes/deployment.yaml

# 6. Start minikube tunnel (in separate terminal)
minikube tunnel  # Leave this running in background

# 7. Verify everything is up
docker ps
kubectl get pods -n mlops
curl http://localhost:8000/health
```

#### Prepare Test Resources

**Create test image for predictions:**
```bash
# Download a sample cat image (small file)
curl -o test_cat.jpg "https://placekitten.com/224/224"

# Or use one from your test dataset
cp data/test/cats/cat.1.jpg test_cat.jpg
```

**Pro Tip:** Keep this file in project root, under 50KB for fast curl uploads.

#### Terminal Configuration

**macOS Terminal Settings:**
1. Preferences → Profiles → Text
2. Font: Menlo, **20pt** (very important - must be readable!)
3. Window size: 120 columns × 30 rows
4. Background: Solid color, slightly dark (easier on eyes)
5. Enable "Use option as meta key"

**Shell prompt:**
```bash
# Simplify your prompt
export PS1="\W $ "  # Shows only current directory

# Or even simpler
export PS1="$ "
```

#### Browser Setup

**Bookmarks to create:**
- http://localhost:5000 (MLflow)
- http://localhost:8000 (API local)
- http://localhost:8000/docs (FastAPI docs)
- https://github.com/YOUR_USERNAME/MLOPS_Assignment2_Group126
- https://github.com/YOUR_USERNAME/MLOPS_Assignment2_Group126/actions
- https://hub.docker.com/r/YOUR_USERNAME/cats-dogs-classifier

**Browser settings:**
- Zoom: 125-150%
- Window size: Full screen
- Clear history/cache (avoid autocomplete suggestions)
- Disable extensions (especially Copilot, Grammarly)
- Use incognito/private mode (clean slate)

### Screen Recording Tools

**Recommended Tools:**

**macOS:**
- **QuickTime Player** (Built-in, free)
  - File → New Screen Recording
  - Quality: Maximum
  - Microphone: Internal or external mic
- **OBS Studio** (Free, professional)
  - More control over sources
  - Can add overlays/graphics
- **Loom** (Free tier, easy sharing)
  - Browser-based
  - Auto-uploads to cloud

**Recommended: QuickTime Player** for simplicity and quality.

**Settings:**
- Resolution: 1920×1080 minimum
- Frame rate: 30fps minimum  
- Audio: Ensure microphone is selected
- Show clicks: Yes (OBS has this option)

### What to Practice Before Recording

**Full Run-Through (3 times):**
1. First time: Get familiar with flow, adjust script
2. Second time: Time yourself (must be under 5 min!)
3. Third time: Record! (or keep practicing if needed)

**Areas that need smooth execution:**
- Switching between terminal and browser
- Typing complex commands (have them in a text file to copy/paste)
- Waiting for outputs (edit out long waits later)
- Timing the kubectl watch/scaling demo

**Commands to pre-test:**
```bash
# Test every command in your script
# Make sure they all work without errors
# Fix any issues before recording
```

### Recording Best Practices

**Golden Rules:**
- **Speak while you act** - No dead air!
- **5 minutes is strict** - If you go over, you MUST cut or re-record
- **Demonstrate, don't explain** - Show it working, narrate what's happening
- **Practice makes perfect** - Do 2-3 dry runs with timing

**Pacing Guidelines:**
- Introduction: 20 seconds (4% of time)
- M1 Model Dev: 30 seconds (10%)
- M2 Containerization: 40 seconds (13%)
- M3 CI: 60 seconds (20%)
- M4 CD/K8s: 70 seconds (23%)
- M5 Monitoring + Flow: 50 seconds (17%)
- Wrap-up: 30 seconds (10%)
- **Buffer: 20 seconds** (for transitions)

**Pro Tips:**
- **Clear terminal before each module** - Type `clear` to avoid clutter
- **Use cursor to point** - When showing output, point at relevant parts
- **Read key outputs briefly** - "Status: healthy, model loaded: true" - helps viewers
- **Speed up where possible** - Fast typing looks professional (or copy/paste long commands)
- **Cut awkward pauses in editing** - Remove waits, hesitations, mistakes
- **Have command cheat sheet** - Text file with all commands in order
- **Disable notifications** - Do Not Disturb mode!
- **Close unnecessary apps** - Slack, email, Messages
- **Check audio levels** - Do a 30-second test recording first
- **Smile in your voice** - Enthusiasm is contagious (even without webcam)

### Common Technical Issues & Fixes

**Port Already in Use**
```bash
# Solution
docker-compose down
lsof -ti:8000 | xargs kill -9  # Kill process on port 8000
```

**Minikube Not Responding**
```bash
# Solution
minikube delete
minikube start --driver=docker
```

**Kubectl Context Wrong**
```bash
# Solution
kubectl config use-context minikube
```

**Docker Image Not in Minikube**
```bash
# Solution (MUST DO THIS!)
minikube image load cats-dogs-classifier:latest

# Verify
minikube image ls | grep cats-dogs
```

**Model File Not Found in Container**
```bash
# Solution - ensure you trained the model first!
python src/train.py --epochs 5  # Quick training

# Or create minimal dummy model for demo
python -c "
from tensorflow import keras
model = keras.Sequential([keras.layers.Dense(1, input_shape=(224,224,3))])
model.save('models/cats_dogs_model.h5')
"
```

**GitHub Actions Not Triggering**
```bash
# Check:
# 1. Actions are enabled in repo settings
# 2. Workflow file has correct indentation (YAML is strict!)
# 3. You pushed to 'main' branch
git branch  # Should show * main
```

**Smoke Tests Failing**
```bash
# Check API_URL is correct
echo $API_URL

# Test manually first
curl $API_URL/health
python tests/smoke_test.py
```

### Editing the Video

**Basic Editing:**
- **Cut long waits**: Docker builds, kubectl wait, etc.
- **Add transitions**: Fade between modules (optional)
- **Add text overlays**: Module names ("M1: Model Development")
- **Speed up boring parts**: 1.25-1.5x speed for repetitive commands
- **Add background music**: Soft, non-intrusive (optional)

**Free Editing Tools:**
- **iMovie** (macOS, simple)
- **DaVinci Resolve** (Professional, free)
- **Shotcut** (Cross-platform, open source)

**YouTube Upload Tips:**
- **Title**: "MLOps Assignment 2 - Cats vs Dogs CI/CD Pipeline - Group 126"
- **Description**: Include GitHub repo link, timestamps for each module
- **Visibility**: Unlisted (only people with link can view)
- **Thumbnail**: Screenshot of your project (optional)

**Video Description Template:**
```
MLOps Assignment 2 - Complete CI/CD Pipeline for Image Classification
Group 126

This video demonstrates a complete end-to-end MLOps pipeline for Cats vs Dogs classification.

GitHub Repository: https://github.com/YOUR_USERNAME/MLOPS_Assignment2_Group126

Timestamps:
0:00 - Introduction
0:20 - M1: Model Development & MLflow
0:50 - M2: Docker Containerization & API
1:30 - M3: CI Pipeline & Automated Testing
2:30 - M4: Kubernetes Deployment & CD
3:40 - M5: Monitoring & Complete CI/CD Flow
4:30 - Summary

Contributors:
- Devaprasad P (2023aa05069)
- Devender Kumar (2024aa05065)
- Chavali Amrutha Valli (2024aa05610)
- Palakolanu Preethi (2024aa05608)
- Rohan Tirthankar Behera (2024aa05607)
```

---

## 5. Quick Command Reference for Video

**Copy these commands - use them in order during recording:**

```bash
# ============================================
# SETUP (Do before recording, not during!)
# ============================================
minikube start
docker-compose up -d
mlflow ui --port 5000 &
kubectl apply -f deployment/kubernetes/deployment.yaml
minikube image load cats-dogs-classifier:latest
curl -o test_cat.jpg "https://placekitten.com/224/224"

# Start minikube tunnel in separate terminal
minikube tunnel

# ============================================
# RECORDING STARTS HERE
# ============================================

# [Intro] Show project structure
clear
ls -la

# [M1] Model Development
head -30 src/model.py
grep -A 3 "mlflow.start_run" src/train.py
open http://localhost:5000  # MLflow UI
cat data.dvc

# [M2] Containerization
head -20 Dockerfile
docker-compose up -d  # If not already running
docker ps
curl http://localhost:8000/health | jq
curl -X POST "http://localhost:8000/predict" -F "file=@test_cat.jpg" | jq

# [M3] CI - Switch to browser
# Navigate to: github.com/YOUR_USERNAME/MLOPS_Assignment2_Group126/actions
# Show latest CI run

# [M4] CD & Kubernetes
clear
kubectl get all -n mlops
kubectl get pods -n mlops
kubectl delete pod cats-dogs-deployment-XXXXX-XXXXX -n mlops
kubectl get pods -n mlops -w  # Watch briefly, then Ctrl+C
kubectl scale deployment cats-dogs-deployment --replicas=5 -n mlops
kubectl get pods -n mlops
curl http://MINIKUBE-IP:PORT/health | jq  # Use your actual URL

# [M5] Monitoring & complete flow
kubectl logs -n mlops deployment/cats-dogs-deployment --tail=15
echo "# CI/CD test" >> README.md
git diff README.md
git add README.md
git commit -m "demonstrate cicd flow"
git push origin main
# Switch to GitHub Actions - show pipeline starting

# [Wrap-up] Final structure
tree -L 2 -I 'venv|__pycache__|.pytest_cache|mlruns|data'
```

---

## 6. Final Submission Checklist

### Before Recording:
- [ ] All commands tested and working
- [ ] Test image (test_cat.jpg) ready in project root
- [ ] Docker containers running (docker-compose up -d)
- [ ] Kubernetes deployed (kubectl get pods -n mlops shows READY)
- [ ] MLflow UI running (http://localhost:5000)
- [ ] Minikube tunnel running (in separate terminal)
- [ ] GitHub Actions workflows have run successfully at least once
- [ ] GitHub secrets configured (DOCKER_USERNAME, DOCKER_PASSWORD, etc.)
- [ ] Terminal font size 20pt
- [ ] Browser zoom 125%
- [ ] All bookmarks created
- [ ] Notifications disabled (Do Not Disturb)
- [ ] Quiet recording environment
- [ ] Script/teleprompter ready
- [ ] Practiced full run-through 2-3 times
- [ ] Timed yourself (MUST be under 5 minutes!)

### During Recording:
- [ ] Clear speaking pace
- [ ] Show commands before executing
- [ ] Use cursor to point at outputs
- [ ] Speak while actions happen (no dead air)
- [ ] Time yourself - stay under 5 minutes!
- [ ] Smooth transitions between modules

### After Recording:
- [ ] Review video for quality (audio, video, timing)
- [ ] Edit out long waits (docker pull, kubectl wait, etc.)
- [ ] Check total runtime (MUST be under 5 minutes!)
- [ ] Add title slide (optional but nice)
- [ ] Add text overlays for modules (optional)
- [ ] Upload to YouTube/Loom
- [ ] Set to Unlisted
- [ ] Test video link in incognito window
- [ ] Add timestamps in description

### GitHub Repository:
- [ ] All code committed
- [ ] .gitignore properly configured
- [ ] No venv/, data/, models/, mlruns/ in git
- [ ] README.md complete with setup instructions
- [ ] requirements.txt has all dependencies
- [ ] .github/workflows/ci.yml present
- [ ] .github/workflows/cd.yml present
- [ ] deployment/kubernetes/deployment.yaml present
- [ ] tests/ folder with 25+ tests
- [ ] Repository is public or accessible to evaluators

### CI/CD Verification:
- [ ] GitHub Actions enabled
- [ ] Secrets configured (check internal/GITHUB_SECRETS_SETUP.md)
- [ ] At least one successful CI run
- [ ] Docker image published to Docker Hub
- [ ] At least one successful CD run (if K8s cluster available)
- [ ] Smoke tests passing

### Final Package:
- [ ] GitHub repository URL
- [ ] Video link (YouTube/Loom/Google Drive)
- [ ] Both links tested from incognito/different device
- [ ] README.md clearly documents how to:
  - [ ] Download dataset from Kaggle
  - [ ] Train the model
  - [ ] Run tests
  - [ ] Build Docker image
  - [ ] Deploy to Kubernetes

---

## 7. Troubleshooting Guide

### Video is Over 5 Minutes

**Solutions:**
1. **Cut out waits** - Remove docker builds, kubectl waits in editing
2. **Speed up sections** - Use 1.25-1.5x speed for slow parts
3. **Trim explanations** - Focus on showing, not explaining every detail
4. **Practice more** - Time yourself, adjust script
5. **Re-record** - If you can't edit down to 5min, record again

### Model File Not in Repository

**This is CORRECT!** Model should NOT be committed.

**In README, document:**
```markdown
## Training the Model

The trained model is not included in the repository (too large).

To generate it:
1. Download dataset: `kaggle competitions download -c dogs-vs-cats`
2. Prepare data: `python src/prepare_dataset.py --source train --output data`
3. Train model: `python src/train.py --epochs 20`

This creates `models/cats_dogs_model.h5` needed for the API.
```

### Dataset Not in Repository

**This is CORRECT!** Dataset should NOT be committed (1GB+).

**In README, document:**
- Link to Kaggle: https://www.kaggle.com/c/dogs-vs-cats
- How to get API credentials
- Commands to download and prepare

### CI/CD Not Working

**Check:**
1. GitHub Actions enabled in repository settings
2. Secrets are configured correctly
3. Workflow files have correct YAML syntax
4. You pushed to `main` branch (not develop or feature branch)
5. Docker Hub credentials are valid
6. Kubernetes cluster is accessible

**Reference:** internal/GITHUB_SECRETS_SETUP.md

### Can't Access Minikube Service

**Solution:**
```bash
# Ensure minikube tunnel is running
minikube tunnel  # Leave this terminal open

# In another terminal, get URL
minikube service cats-dogs-service -n mlops --url

# Check pods are running
kubectl get pods -n mlops

# Check service exists
kubectl get svc -n mlops
```

### Python Version Issues

**Error**: `ModuleNotFoundError: No module named 'tensorflow'`

**Cause**: Python 3.13 doesn't support TensorFlow 2.13

**Solution**: Use Python 3.9, 3.10, or 3.11
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker Build Fails - COPY models/

**Error**: `COPY failed: file not found models/cats_dogs_model.h5`

**Solutions:**

**Option 1**: Train the model first
```bash
python src/train.py --epochs 5
docker build -t cats-dogs-classifier:latest .
```

**Option 2**: Create dummy model for testing
```python
python -c "
from tensorflow import keras
model = keras.Sequential([keras.layers.Dense(1, input_shape=(224,224,3))])
model.save('models/cats_dogs_model.h5')
"
docker build -t cats-dogs-classifier:latest .
```

**Note**: CI workflow creates dummy model automatically for build testing!

---

## 8. Submission Day Checklist

### 48 Hours Before Deadline:
- [ ] Complete final testing of entire workflow
- [ ] Record video (practice twice, record on third try)
- [ ] Upload video and test link
- [ ] Push all code to GitHub
- [ ] Verify GitHub Actions ran successfully
- [ ] Document any known issues in README

### 24 Hours Before Deadline:
- [ ] Review video one more time (quality, timing, content)
- [ ] Test GitHub link in incognito mode
- [ ] Test video link from different device
- [ ] Ensure README is complete and clear
- [ ] Check all file paths in README are correct
- [ ] Verify submission format matches assignment requirements

### Day of Submission:
- [ ] Final check: video under 5 minutes
- [ ] Final check: GitHub repository accessible
- [ ] Final check: video link works
- [ ] Prepare submission text file:

```
MLOps Assignment 2 - Group 126

GitHub Repository: https://github.com/YOUR_USERNAME/MLOPS_Assignment2_Group126
Video Demonstration: https://youtube.com/watch?v=XXXXX

Contributors:
- Devaprasad P (2023aa05069)
- Devender Kumar (2024aa05065)
- Chavali Amrutha Valli (2024aa05610)
- Palakolanu Preethi (2024aa05608)
- Rohan Tirthankar Behera (2024aa05607)

All 5 modules implemented:
✅ M1: Model Development & Experiment Tracking (MLflow, DVC)
✅ M2: Model Packaging & Containerization (FastAPI, Docker)
✅ M3: CI Pipeline (GitHub Actions, pytest, Docker Hub)
✅ M4: CD Pipeline & Deployment (Kubernetes, smoke tests)
✅ M5: Monitoring & Logging (Structured logs, metrics tracking)
```

- [ ] Submit through official channel
- [ ] Keep backup of all files locally
- [ ] Celebrate! 🎉

---

**Good luck with your submission! Remember: 5 minutes maximum, show the complete workflow, and demonstrate all 5 modules working together. You've got this! 🚀**
