# NyayLens - Architecture Diagram

## System Flow

```mermaid
flowchart TB
    subgraph Frontend["🖥️ Frontend (Vanilla JS)"]
        UI[User Interface]
        Auth[Auth Token Storage]
    end
    
    subgraph Backend["⚙️ FastAPI Backend"]
        API[API Endpoints<br/>13 routes]
        AuthM[JWT Auth]
        Valid[Input Validation]
        Logger[JSON Logger]
    end
    
    subgraph NewsIngestion["📰 News Ingestion"]
        RSS[RSS Feeds<br/>8 sources]
        Custom[Custom URL<br/>Ingestion]
        Parser[Article Parser<br/>newspaper3k]
    end
    
    subgraph NLP["🧠 NLP Pipeline"]
        Classify[Topic Classification<br/>spaCy + Keywords]
        Extract[Entity Extraction<br/>NER]
        LLM[LLM Integration<br/>OpenAI GPT-3.5<br/>Optional]
        Lemma[Lemmatization<br/>spaCy]
    end
    
    subgraph Severity["📊 Severity Scoring"]
        Keywords[Weighted Keywords<br/>3 tiers]
        Multiplier[Multipliers<br/>minors: 1.3x<br/>mass: 1.25x]
    end
    
    subgraph RAG["📚 RAG System"]
        ConstDB[(Constitutional DB<br/>8 FRs + 5 DPSPs<br/>30+ case laws)]
        PDFExtract[PDF Extractor<br/>1019 chunks]
        Embeddings[Sentence Transformers<br/>all-mpnet-base-v2]
        FAISS[FAISS Index<br/>1064 documents]
        Relevance[Relevance Filter<br/>≥30% threshold]
    end
    
    subgraph PILGen["📄 PIL Generation"]
        Template[PIL Template]
        Validator[Citation Validator<br/>SC/HC compliance]
        PDFGen[PDF Generator<br/>reportlab]
    end
    
    subgraph Storage["💾 Data Storage"]
        PostgreSQL[(PostgreSQL<br/>News Articles)]
        JSON[(JSON Fallback<br/>legacy support)]
        Cache[(Embedding Cache<br/>8.6min build)]
    end
    
    %% Main Flow
    UI -->|HTTP Request| API
    API -->|Verify| AuthM
    API -->|Validate| Valid
    API -->|Log| Logger
    
    %% News Ingestion Flow
    API -->|Fetch News| RSS
    API -->|Add Custom| Custom
    RSS -->|Parse| Parser
    Custom -->|Parse| Parser
    Parser -->|Store| PostgreSQL
    Parser -->|Fallback| JSON
    
    %% NLP Flow
    Parser -->|Text| Classify
    Parser -->|Text| Extract
    Classify -->|Enhanced| LLM
    Classify -->|Severity| Lemma
    Lemma -->|Score| Keywords
    Keywords -->|Apply| Multiplier
    
    %% RAG Flow
    API -->|Query| ConstDB
    API -->|Search PDFs| PDFExtract
    PDFExtract -->|Embed| Embeddings
    Embeddings -->|Index| FAISS
    FAISS -->|Load| Cache
    FAISS -->|Filter| Relevance
    ConstDB -->|Retrieve| Relevance
    
    %% PIL Generation Flow
    Relevance -->|Legal Refs| Template
    Extract -->|Entities| Template
    Classify -->|Topics| Template
    Multiplier -->|Severity| Template
    Template -->|Validate| Validator
    Validator -->|Generate| PDFGen
    PDFGen -->|Download| UI
    
    %% Styling
    classDef frontend fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef backend fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef nlp fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef rag fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef storage fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    
    class UI,Auth frontend
    class API,AuthM,Valid,Logger backend
    class Classify,Extract,LLM,Lemma nlp
    class ConstDB,PDFExtract,Embeddings,FAISS,Relevance rag
    class PostgreSQL,JSON,Cache storage
```

## Data Flow Detail

### 1. News Ingestion → Storage
```
RSS Feeds (8 sources) 
  → feedparser 
  → newspaper3k (title, text, date)
  → Topic Classification (spaCy NLP + keywords)
  → Entity Extraction (NER: PERSON, ORG, GPE, LAW)
  → Severity Scoring (lemmatized keywords + multipliers)
  → PostgreSQL (NewsArticle table)
```

### 2. Semantic Search Index Build
```
Legal PDFs (RTI, EP Act, BNSS, etc.)
  → pdfminer.six (text extraction)
  → Chunking (400 words, 80 overlap)
  → Constitutional DB (FRs, DPSPs, case laws)
  → sentence-transformers (all-mpnet-base-v2)
  → FAISS IndexFlatIP (cosine similarity)
  → Pickle cache (data/semantic_cache.pkl)
```

### 3. PIL Generation Pipeline
```
User selects article (index)
  → Fetch from PostgreSQL
  → Extract issue (spaCy NER or OpenAI)
  → Retrieve legal sections:
      - ConstDB by topic mapping
      - Semantic search (FAISS, ≥30% similarity)
  → Generate PIL (pil_template.txt)
  → Validate citations (PIL Validator)
  → Export PDF (reportlab)
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vanilla JS, HTML5, CSS3 |
| **Backend** | FastAPI 0.104+, Uvicorn |
| **NLP** | spaCy 3.8, sentence-transformers 5.2 |
| **LLM** | OpenAI GPT-3.5-turbo (optional) |
| **Vector DB** | FAISS-CPU 1.13, chromadb 1.4 |
| **Database** | PostgreSQL (via SQLAlchemy 2.0) |
| **Auth** | JWT (python-jose) |
| **PDF** | reportlab 4.4, pdfminer.six |
| **Testing** | pytest 9.0, pytest-cov 7.0 |

## Key Metrics

- **Legal Documents Indexed**: 1,064 (45 constitutional + 1,019 PDF chunks)
- **Embedding Dimension**: 768 (all-mpnet-base-v2)
- **Relevance Threshold**: 30% cosine similarity
- **Cache Build Time**: 8.6 minutes (one-time)
- **API Endpoints**: 13 routes
- **Test Coverage**: 60+ tests across 9 modules

## Deployment Architecture (Recommended)

```mermaid
graph LR
    subgraph Production
        LB[Load Balancer<br/>nginx]
        API1[FastAPI<br/>Instance 1]
        API2[FastAPI<br/>Instance 2]
        PG[(PostgreSQL<br/>Primary)]
        Redis[(Redis<br/>Cache)]
        S3[S3<br/>PDF Storage]
    end
    
    Client -->|HTTPS| LB
    LB --> API1
    LB --> API2
    API1 --> PG
    API2 --> PG
    API1 --> Redis
    API2 --> Redis
    API1 --> S3
    API2 --> S3
```

---

**Generated**: January 24, 2026  
**Project**: NyayLens - AI-Powered PIL Generator  
**Architecture**: Microservices-ready, RAG-enhanced legal tech system
