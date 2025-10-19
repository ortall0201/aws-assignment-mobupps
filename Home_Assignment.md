# ML Engineer at MobUpps
## Home Assignment

### Background
You are joining a Data Science team at an AdTech company that helps advertisers find the right audience for new mobile applications. The team has developed ML models that analyze app similarities and predict campaign performance.

Your role will be to build and maintain the production infrastructure for these models, implement A/B testing frameworks, and ensure reliable model deployment.

### Provided Files
You have received the following anonymized data files:
- `mock_embeddings_v1.pkl` - App embeddings from model version 1
- `mock_embeddings_v2.pkl` - App embeddings from model version 2  
- `sample_apps.csv` - Application metadata
- `historical_performance.csv` - Past campaign performance metrics
- `README.md` - Data format documentation

### Assignment

#### Part A: Architecture Design (1.5 hours)

Design a complete ML production system on AWS for the following use case:
- **Input**: New app metadata
- **Process**: Find 10-20 similar apps using embeddings
- **Output**: Predicted performance score and user segments

**Deliverables:**
1. **System Architecture Diagram** 
   - Use any tool (draw.io, lucidchart, or even hand-drawn + photo)
   - Show data flow from ingestion to serving
   - Include feedback loop for model improvement
   - Mark AWS services clearly

2. **Technical Design Document** (1-2 pages)
   - AWS services selection and justification
   - A/B testing strategy for comparing v1 vs v2 models
   - CI/CD pipeline overview
   - Monitoring and alerting approach
   - Scaling considerations (from 100 to 1M requests/day)
   - Cost optimization strategies

#### Part B: Local Implementation (2 hours)

Implement a production-ready similarity service that demonstrates your coding abilities.

**Core Requirements:**

1. **Similarity Service**
```python
class SimilarityService:
    """
    Load embeddings and find similar apps
    - Support both v1 and v2 embeddings
    - Efficient similarity search
    - Performance metrics collection
    """
```

2. **A/B Testing Framework**
```python
class ABTestController:
    """
    Route traffic between model versions
    - Configurable traffic split (e.g., 70/30)
    - Track performance per version
    - Decision logic for winner selection
    """
```

3. **REST API**
   - `POST /find-similar` - Find similar apps
   - `GET /health` - Health check
   - `GET /metrics` - Performance metrics
   - `POST /predict` - Predict performance (optional)

4. **Production Requirements**
   - Docker containerization (docker-compose)
   - Configuration management (YAML/env)
   - Comprehensive error handling
   - Structured logging
   - Unit tests (pytest)
   - Performance test showing <200ms latency

**Project Structure:**
```
your_solution/
├── src/
│   ├── services/
│   │   ├── similarity.py
│   │   └── ab_testing.py
│   ├── api/
│   │   └── endpoints.py
│   └── config/
│       └── config.yaml
├── tests/
│   └── test_similarity.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
└── README.md
```

#### Part C: Bonus (Optional - 30 minutes)

Choose one or more:
- Implement caching layer for embeddings
- Add batch processing endpoint
- Propose optimization for similarity search (e.g., use of index structures)
- Create basic CI/CD pipeline (GitHub Actions)
- Implement feature drift detection

### Evaluation Criteria

**We will evaluate:**
- Architecture thinking and AWS knowledge
- Code quality and design patterns
- Production-readiness mindset
- A/B testing implementation
- Documentation quality
- Performance considerations

**Red Flags:**
- No error handling
- No tests
- Ignoring A/B testing requirement
- Poor performance (>500ms latency)

**Green Flags:**
- Clean, modular code
- Comprehensive testing
- Thoughtful architecture
- Performance optimizations
- Good documentation

### Submission

Please submit:
1. Architecture diagram (PDF/PNG)
2. Technical design document (PDF/MD)
3. Code repository (ZIP or GitHub link)
4. README with setup instructions

**Time Limit:** 3-4 hours


### Notes
- Focus on production-readiness, not model development
- The embeddings are pre-trained; you don't need to modify them
- Feel free to use any Python libraries you find appropriate
- Document any assumptions you make



Good luck!