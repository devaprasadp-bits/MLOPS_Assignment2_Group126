# Screen Recording Script Guide

## Recording Requirements

- **Duration**: Maximum 5 minutes
- **Format**: MP4, MOV, or WebM
- **Resolution**: 1280x720 minimum (1920x1080 recommended)
- **Audio**: Optional but recommended for narration

## Timeline Breakdown

### 0:00 - 0:30 - Introduction & Setup (30 seconds)
- Show project structure in VS Code/IDE
- Briefly show README.md
- Make a small code change (e.g., update a comment or parameter)
- `git add .`
- `git commit -m "Demo: Update model parameter"`
- `git push origin main`

### 0:30 - 1:30 - CI Pipeline (60 seconds)
- Switch to GitHub repository in browser
- Navigate to Actions tab
- Show CI pipeline starting automatically
- Highlight the stages:
  - Checkout code
  - Install dependencies
  - Run unit tests (show tests passing)
  - Build Docker image
  - Push to registry

### 1:30 - 2:00 - Docker Image (30 seconds)
- Show Docker Hub or GitHub Container Registry
- Show the newly pushed image with tag
- Highlight image size and timestamp

### 2:00 - 3:00 - CD Pipeline & Deployment (60 seconds)
- Show CD pipeline triggered automatically
- Highlight deployment steps:
  - Pull image from registry
  - Update Kubernetes deployment
  - Wait for rollout
  - Run smoke tests
- Show smoke tests passing

### 3:00 - 3:30 - Smoke Tests Detail (30 seconds)
- Show smoke test output/logs
- Health check: ✓ PASSED
- Prediction test: ✓ PASSED
- Invalid input test: ✓ PASSED

### 3:30 - 4:30 - Live Prediction (60 seconds)
- Open terminal
- Test health endpoint: `curl http://<api-url>/health`
- Show healthy response with metrics
- Test prediction with an image:
  - Show the cat/dog image
  - Run curl command or Postman
  - Show prediction result with class and probability
- Try another image (opposite class)
- Show quick response time

### 4:30 - 5:00 - Monitoring & Conclusion (30 seconds)
- Show MLflow UI with training metrics
- Show logs or monitoring dashboard
- Quick look at Kubernetes pods: `kubectl get pods -n mlops`
- Conclude by showing all components working together

## Recording Tools

### macOS
- **QuickTime Player** (Built-in, free)
- **OBS Studio** (Free, open-source)
- **ScreenFlow** (Paid, professional)

### Windows
- **OBS Studio** (Free, open-source)
- **Camtasia** (Paid, professional)
- **Xbox Game Bar** (Built-in, Win+G)

### Linux
- **OBS Studio** (Free, open-source)
- **SimpleScreenRecorder** (Free, simple)
- **Kazam** (Free, easy to use)

## Recording Checklist

### Before Recording
- [ ] Close unnecessary applications
- [ ] Clean up desktop/workspace
- [ ] Prepare browser tabs in order
- [ ] Test all commands beforehand
- [ ] Ensure stable internet connection
- [ ] Set screen resolution to 1920x1080
- [ ] Turn off notifications
- [ ] Clear terminal history for clean output
- [ ] Have test images ready
- [ ] Practice the flow 2-3 times

### During Recording
- [ ] Start recording
- [ ] Speak clearly if adding narration
- [ ] Move cursor deliberately (not too fast)
- [ ] Pause briefly between sections
- [ ] Show outputs completely
- [ ] Avoid scrolling too fast
- [ ] Keep within 5-minute limit

### After Recording
- [ ] Review the recording
- [ ] Check audio quality (if used)
- [ ] Verify all requirements shown
- [ ] Trim unnecessary parts
- [ ] Export in compatible format
- [ ] Test playback
- [ ] Check file size

## Script Template

```
[0:00] "Welcome. This is a demonstration of our MLOps pipeline for 
       Cats vs Dogs classification. I'll show the complete workflow 
       from code change to deployed prediction."

[0:10] "Here's our project structure. I'll make a small change and 
       push to GitHub."
       [Show git commands]

[0:30] "The CI pipeline starts automatically. Tests are running..."
       [Show GitHub Actions]

[1:00] "All tests passed. Docker image is being built and pushed 
       to the registry."

[1:30] "Here's the image in Docker Hub."
       [Show registry]

[2:00] "CD pipeline deploys to Kubernetes automatically."
       [Show CD workflow]

[3:00] "Smoke tests are running to verify the deployment."
       [Show test output]

[3:30] "Let's test the live API. First, a health check..."
       [Run curl command]

[3:45] "Now a prediction on this cat image..."
       [Show prediction]

[4:00] "And here's a dog image..."
       [Show prediction]

[4:30] "Here's our MLflow dashboard with training metrics..."
       [Show MLflow]

[4:45] "All components are working together - from code to 
       deployment. Thank you."
```

## Quick Recording Script

If short on time, use OBS Studio:

```bash
# macOS/Linux
brew install obs

# Configure scene
# - Display Capture for full screen
# - Window Capture for specific windows
# - Text overlays for annotations

# Recording settings
# - Format: MP4
# - Encoder: x264
# - Bitrate: 2500 Kbps
# - Resolution: 1920x1080
# - FPS: 30
```

## Editing Tips

### Quick Edits (if needed)
- Trim start/end silence
- Speed up slow parts (1.5x)
- Add title screen (3 seconds)
- Add end screen (2 seconds)
- Export with good compression

### Tools for Editing
- **iMovie** (macOS, free)
- **DaVinci Resolve** (Cross-platform, free)
- **Shotcut** (Cross-platform, free)
- **OpenShot** (Cross-platform, free)

## Upload Options

### If File Too Large

1. **YouTube (Unlisted)**
   - Upload as unlisted video
   - Share link in submission

2. **Google Drive**
   - Upload to Drive
   - Share link with view permissions

3. **Compress Video**
   ```bash
   # Using ffmpeg
   ffmpeg -i input.mov -vcodec h264 -acodec aac output.mp4
   ```

## Final Checks

- [ ] Duration under 5 minutes
- [ ] All 5 modules demonstrated
- [ ] Code change visible
- [ ] CI pipeline shown
- [ ] CD deployment shown
- [ ] Live predictions working
- [ ] Monitoring visible
- [ ] Audio clear (if included)
- [ ] No sensitive information shown
- [ ] File size reasonable (<500MB)

## Example Command Sequence

```bash
# For easy copy-paste during recording

# 1. Code change
git add .
git commit -m "Demo: MLOps workflow"
git push origin main

# 2. Check CI
# (Open GitHub Actions in browser)

# 3. Check deployment
kubectl get pods -n mlops
kubectl get svc -n mlops

# 4. Test API
export API_URL=http://localhost:8000
curl $API_URL/health

# 5. Prediction
curl -X POST "$API_URL/predict" \
  -F "file=@data/test/cats/cat.1000.jpg"

curl -X POST "$API_URL/predict" \
  -F "file=@data/test/dogs/dog.1000.jpg"

# 6. View metrics
# (Open MLflow UI: http://localhost:5000)
```

Good luck with your recording!
