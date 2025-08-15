# TrueCast: Real-time News RAG with Fact-Checking

A comprehensive real-time news retrieval and fact-checking system that continuously ingests news articles, identifies potential misinformation, and provides fact-checked responses with source verification and credibility scoring.

## 🚀 Features

### Core Functionality
- **Real-time News Ingestion**: Automated RSS feed processing from major financial news sources
- **Vector-based Retrieval**: Semantic search using ChromaDB and sentence transformers
- **Misinformation Detection**: NLI-based stance detection and claim verification
- **Source Credibility Assessment**: Domain-based reliability scoring
- **Fact-checked Responses**: AI-generated answers with citations and credibility scores

### Technical Components
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` for semantic search
- **Reranking**: `cross-encoder/ms-marco-MiniLM-L-6-v2` for improved retrieval
- **NLI Model**: `facebook/bart-large-mnli` for stance detection
- **LLM**: OpenAI GPT-4 for fact-checked answer generation
- **Vector Database**: ChromaDB for persistent storage
- **Web Interface**: Streamlit for user interaction

## 📋 Requirements

- Python 3.9+
- OpenAI API key
- Internet connection for news ingestion

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd news-rag-factcheck
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## 🚀 Usage

### Starting the Application

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app/main.py --server.port 8501
   ```

3. **Open your browser** and navigate to `http://localhost:8501`

### Using the Application

The application has three main tabs:

#### 1. Ask a Question
- Enter any question about recent news
- Get fact-checked answers with source citations
- View credibility scores and misinformation flags

#### 2. Check a Claim
- Enter a specific claim to verify
- Get stance analysis against retrieved evidence
- View supporting/contradicting sources

#### 3. Manage Feeds
- Manually trigger news ingestion
- Add individual articles via URL
- Monitor ingestion status

## 🏗️ Architecture

```
news-rag-factcheck/
├── app/
│   └── main.py              # Streamlit web interface
├── core/
│   ├── config.py            # Configuration management
│   ├── ingestion.py         # RSS feed processing
│   ├── indexing.py          # Vector database operations
│   ├── retriever.py         # Semantic search and reranking
│   ├── generator.py         # LLM-based answer generation
│   ├── misinfo.py           # Misinformation detection
│   ├── credibility.py       # Source credibility assessment
│   └── utils.py             # Utility functions
├── data/
│   ├── feeds_finance.yaml   # RSS feed configurations
│   ├── domain_policies.json # Source credibility scores
│   └── chroma/              # Vector database storage
└── requirements.txt         # Python dependencies
```

## 🔧 Configuration

### RSS Feeds
Edit `data/feeds_finance.yaml` to add or modify news sources:
```yaml
sources:
  - name: Reuters Business
    type: rss
    url: https://feeds.reuters.com/reuters/businessNews
```

### Source Credibility
Edit `data/domain_policies.json` to set credibility scores (0-100):
```json
{
    "reuters.com": 90,
    "ft.com": 85,
    "cnbc.com": 80
}
```

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `MODEL_EMBED`: Embedding model (default: sentence-transformers/all-MiniLM-L6-v2)
- `CHUNK_SIZE`: Text chunk size for indexing (default: 500)
- `TOP_K`: Number of retrieved documents (default: 5)

## 📊 System Performance

### Current Capabilities
- **Ingestion Rate**: ~50 articles per run from 5 major sources
- **Retrieval Speed**: <2 seconds for semantic search
- **Fact-checking**: Real-time claim verification with NLI
- **Credibility Scoring**: Domain-based reliability assessment

### Data Sources
- Reuters Business News
- Financial Times
- CNBC Finance
- Yahoo Finance
- Bloomberg Markets

## 🔍 Fact-Checking Process

1. **Query Processing**: User question is processed for semantic search
2. **Retrieval**: Top-k relevant articles are retrieved from vector database
3. **Reranking**: Retrieved documents are reranked for relevance
4. **Evidence Analysis**: For claims, NLI model analyzes stance against evidence
5. **Answer Generation**: LLM generates fact-checked response with citations
6. **Credibility Assessment**: Source reliability scores are computed

## 🛡️ Misinformation Detection

The system uses Natural Language Inference (NLI) to:
- Compare claims against retrieved evidence
- Identify supporting, contradicting, or neutral sources
- Flag potential misinformation based on evidence balance
- Provide confidence scores for stance detection

## 📈 Evaluation Metrics

- **Retrieval Accuracy**: Semantic similarity matching
- **Response Quality**: Fact-checked answers with citations
- **Misinformation Detection**: Stance analysis accuracy
- **Source Credibility**: Domain-based reliability scoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Hugging Face for transformer models
- ChromaDB for vector database
- Streamlit for web interface framework

## 📞 Support

For issues and questions, please open an issue on the GitHub repository.

---

**TrueCast** - Empowering fact-checked news consumption through AI-powered RAG systems.
