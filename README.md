# NexFlow Fraud Detection System

## 🎯 Project Overview

NexFlow is a comprehensive fraud detection system designed to identify and prevent fraudulent transactions in real-time. This project combines advanced machine learning techniques, natural language processing, and sophisticated feature engineering to create a robust fraud detection pipeline.

### Key Features
- **Real-time Fraud Detection**: Detect fraudulent transactions with 95.7% accuracy
- **Advanced Feature Engineering**: 15+ engineered features for pattern recognition
- **NLP Integration**: Process and analyze merchant reviews for fraud indicators
- **Web Scraping Pipeline**: Automated data extraction from e-commerce sites
- **Interactive Dashboard**: Streamlit-based interface for transaction monitoring
- **Model Explainability**: SHAP values for transparent decision-making

## 📊 Dataset Information

### Primary Dataset
- **Size**: 1,000,000 transactions
- **Format**: CSV (nexflow_master_dataset.csv)
- **Target Variable**: `is_fraudulent` (0/1)
- **Class Distribution**: 82% legitimate, 18% fraudulent

### Data Schema
| Column | Type | Description |
|--------|------|-------------|
| `transaction_id` | String | Unique transaction identifier |
| `user_id` | String | User account identifier |
| `transaction_amount` | Float | Transaction value in USD |
| `transaction_timestamp` | DateTime | Transaction timestamp |
| `user_location` | String | User's geographical location |
| `merchant_location` | String | Merchant's geographical location |
| `merchant_category` | String | Category of merchant |
| `merchant_name` | String | Merchant website/name |
| `device_id` | String | Device fingerprint |
| `device_type` | String | Device type (Mobile/Desktop/Tablet) |
| `payment_method` | String | Payment method used |
| `account_balance` | Float | User's account balance |
| `transaction_status` | String | Transaction status |
| `ip_address` | String | IP address used |
| `is_fraudulent` | Integer | Target variable (0/1) |

## 🏗️ Project Architecture

### Directory Structure
```
Fraud Detection/
├── Data Extraction/              # Web scraping pipeline
│   ├── main_extraction.py       # Main extraction orchestrator
│   ├── scrapers/                # Web scraping modules
│   │   ├── static_scraper.py   # Static site scraping
│   │   └── dynamic_scraper.py  # Dynamic site scraping
│   └── utils/                   # Utility functions
│       ├── config.py           # Configuration settings
│       └── file_handler.py     # File I/O operations
├── Data Preprocessing Pipeline/  # Data cleaning & feature engineering
│   └── Data_Pipeline.ipynb     # Jupyter notebook for preprocessing
├── NLP Pipeline/                # Natural language processing
│   ├── process_reviews.py      # Review processing pipeline
│   ├── merge_data_sources.py  # Data merging logic
│   └── spacy_extractor.py     # Entity extraction using spaCy
├── Synthetic Generation/        # Data augmentation
│   └── data_synthesizer.py    # Generate synthetic transactions
├── Interface/                   # User interface
│   └── app.py                 # Streamlit dashboard
├── Saved Models/               # Trained models
│   └── xgb_model_tuned.pkl   # Tuned XGBoost model
├── Data/                      # Data storage
│   ├── raw/                  # Raw scraped data
│   ├── processed/            # Processed data
│   └── final/               # Final datasets
├── Test Data/               # Testing datasets
├── Practice/               # Development experiments
└── run_all.py             # Complete pipeline orchestrator
```

## 🔄 Workflow Pipeline

### 1. Data Extraction Phase
```bash
python "Data Extraction/main_extraction.py"
```
- **Static Scraping**: Extract merchant categories, pricing, and basic information
- **Dynamic Scraping**: Collect user reviews and transaction data
- **Batch Processing**: Save data in chunks to prevent data loss

### 2. NLP Processing Phase
```bash
python "nlp_pipeline/process_reviews.py"
```
- **Entity Extraction**: Use spaCy to extract transaction amounts, locations, and categories
- **Fraud Heuristics**: Apply rule-based fraud detection on review text
- **Structured Output**: Convert unstructured text to structured data

### 3. Data Merging Phase
```bash
python "nlp_pipeline/merge_data_sources.py"
```
- **Data Integration**: Merge scraped and processed data
- **Quality Assurance**: Ensure data consistency and completeness
- **Master Seed Creation**: Generate seed data for synthetic generation

### 4. Synthetic Data Generation
```bash
python "synthetic_generation/data_synthesizer.py"
```
- **Scale to 1M rows**: Generate realistic transaction data
- **Overlapping Distributions**: Create realistic fraud/legitimate patterns
- **Probabilistic Features**: Maintain statistical consistency

### 5. Model Training & Evaluation
```python
# Execute in Data_Pipeline.ipynb
```
- **Data Preprocessing**: Clean and engineer features
- **Model Comparison**: Test Random Forest, AdaBoost, and XGBoost
- **Hyperparameter Tuning**: Optimize XGBoost for best performance
- **Model Persistence**: Save best model for deployment

### 6. Deployment & Monitoring
```bash
streamlit run interface/app.py
```
- **Real-time Inference**: Process new transactions
- **Performance Metrics**: Track accuracy, precision, recall
- **Explainability**: SHAP values for model transparency

## 🧠 Feature Engineering

### Core Features
1. **Transaction Velocity**: Number of transactions per device in last hour
2. **Balance-to-Amount Ratio**: `transaction_amount / account_balance`
3. **Night Outlier**: High-value transactions between 1-4 AM
4. **Location Change**: Same user in different locations within 3 hours
5. **Device Type Encoding**: Mobile (-1), Desktop (0), Tablet (1)
6. **Payment Method Encoding**: Risk-based encoding
7. **Merchant Category Encoding**: Fraud rate by category
8. **Merchant Name Encoding**: Historical fraud patterns

### Advanced Features
- **Duplicate Transaction Flag**: Detect duplicate transaction IDs
- **Negative Transaction Flag**: Flag invalid negative amounts
- **Invalid IP Flag**: Detect malformed IP addresses
- **Transaction Status Encoding**: Fraud likelihood by status

## 🤖 Machine Learning Models

### Model Comparison Results
| Model | Accuracy | Precision | Recall | F1-Score | AUC-ROC |
|-------|----------|-----------|--------|----------|---------|
| **XGBoost (Tuned)** | **95.76%** | **89.16%** | **86.83%** | **87.98%** | **92.26%** |
| AdaBoost | 95.49% | 89.38% | 84.83% | 87.05% | 91.32% |
| Random Forest | 94.35% | 84.09% | 84.34% | 84.22% | 90.43% |

### Final Model: XGBoost
```python
# Best Hyperparameters
{
    'n_estimators': 500,
    'max_depth': 7,
    'learning_rate': 0.1,
    'subsample': 0.9,
    'colsample_bytree': 0.8
}
```

## 📈 Performance Metrics

### Key Performance Indicators
- **Accuracy**: 95.76% - Overall correct predictions
- **Precision**: 89.16% - Minimize false positives
- **Recall**: 86.83% - Catch maximum fraud cases
- **F1-Score**: 87.98% - Balanced performance
- **AUC-ROC**: 92.26% - Ranking ability

### Business Impact
- **False Positive Rate**: 10.84% - Legitimate transactions flagged
- **False Negative Rate**: 13.17% - Fraud cases missed
- **Processing Speed**: <100ms per transaction
- **Scalability**: Handles 1M+ transactions efficiently

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Required Libraries
```bash
pip install pandas numpy scikit-learn xgboost streamlit
pip install matplotlib seaborn shap spacy faker
pip install beautifulsoup4 selenium requests
```

### spaCy Model Setup
```bash
python -m spacy download en_core_web_sm
```

### Quick Start
1. **Clone the repository**
2. **Run the complete pipeline**:
   ```bash
   python run_all.py
   ```
3. **Launch the dashboard**:
   ```bash
   streamlit run interface/app.py
   ```

## 📊 Data Sources & Collection

### Web Scraping Strategy
- **Static Sites**: Extract product information, pricing, categories
- **Dynamic Sites**: Collect user reviews and ratings
- **Target Merchants**: Amazon, eBay, Newegg, ASOS, Shein, TripAdvisor

### Data Quality Assurance
- **Validation Rules**: IP address validation, amount ranges
- **Duplicate Detection**: Transaction ID uniqueness checks
- **Missing Value Handling**: Comprehensive null value checks
- **Data Type Consistency**: Ensure proper data types

## 🔧 Configuration

### Key Configuration Files
- **`Data Extraction/utils/config.py`**: Scraping targets and settings
- **Model Parameters**: Stored in `saved models/xgb_model_tuned.pkl`
- **Feature Encodings**: Pre-calculated mappings in `interface/app.py`

### Environment Variables
```python
# Data paths
DATA_RAW_PATH = "data/raw/"
DATA_PROCESSED_PATH = "data/processed/"
DATA_FINAL_PATH = "data/final/"

# Model paths
MODEL_PATH = "saved models/xgb_model_tuned.pkl"

# Scraping settings
MAX_PAGES_STATIC = 5
MAX_PAGES_DYNAMIC = 3
```

## 🚀 Usage Examples

### Batch Processing
```python
# Process entire dataset
python run_all.py

# Individual pipeline stages
python "Data Extraction/main_extraction.py"
python "nlp_pipeline/process_reviews.py"
python "synthetic_generation/data_synthesizer.py"
```

### Real-time Prediction
```python
import pickle
import pandas as pd

# Load model
with open('saved models/xgb_model_tuned.pkl', 'rb') as f:
    model = pickle.load(f)

# Prepare data (same preprocessing as training)
X_processed, _ = preprocess_data(new_transactions)

# Make predictions
predictions = model.predict(X_processed)
probabilities = model.predict_proba(X_processed)[:, 1]
```

### Interactive Dashboard
1. Upload transaction CSV via sidebar
2. Choose evaluation mode (with/without labels)
3. View real-time predictions and metrics
4. Analyze SHAP explanations for model decisions

## 🔍 Model Explainability

### SHAP Analysis
- **Feature Importance**: Visualize which features drive fraud decisions
- **Individual Explanations**: Understand specific transaction predictions
- **Global Patterns**: Identify systemic fraud indicators

### Key Fraud Indicators
1. **High Transaction Velocity**: Multiple transactions from same device
2. **Unusual Location Patterns**: Rapid location changes
3. **Night-time Large Transactions**: Suspicious timing patterns
4. **High Balance-to-Amount Ratios**: Account draining behavior
5. **Suspicious IP Addresses**: Invalid or proxy IPs

## 📝 API Reference

### Core Functions

#### `preprocess_data(df, has_labels=True)`
Preprocess raw transaction data for model prediction.

**Parameters:**
- `df`: Raw transaction DataFrame
- `has_labels`: Boolean indicating if target variable present

**Returns:**
- `X`: Processed features DataFrame
- `y_true`: Target variable (if available)

#### `check_ip(ip)`
Validate IP address format.

**Parameters:**
- `ip`: IP address string

**Returns:**
- `0`: Valid IP
- `1`: Invalid IP

### Model Interface
```python
# Load model
model = load_model()

# Predict
predictions = model.predict(X)
probabilities = model.predict_proba(X)[:, 1]

# Explain with SHAP
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)
```

## 🧪 Testing & Validation

### Test Data Structure
- **Location**: `test data/` directory
- **Format**: CSV files matching production schema
- **Size**: Various sizes for performance testing

### Validation Metrics
- **Cross-validation**: 5-fold CV on training data
- **Holdout Test**: 10% separate test set
- **Performance Monitoring**: Real-time metric tracking

## 🔄 Continuous Integration

### Pipeline Automation
```bash
# Complete pipeline execution
python run_all.py

# Individual stage execution
python "Data Extraction/main_extraction.py"
python "nlp_pipeline/process_reviews.py"
python "nlp_pipeline/merge_data_sources.py"
python "synthetic_generation/data_synthesizer.py"
```

### Model Retraining
1. **Data Collection**: Gather new transaction data
2. **Feature Engineering**: Apply same preprocessing pipeline
3. **Model Training**: Retrain with updated hyperparameters
4. **Validation**: Test against holdout dataset
5. **Deployment**: Replace production model

## 📊 Monitoring & Maintenance

### Performance Monitoring
- **Accuracy Tracking**: Monitor model drift over time
- **Feature Distribution**: Track feature distribution changes
- **Latency Monitoring**: Ensure real-time performance
- **Error Analysis**: Track and analyze prediction errors

### Maintenance Schedule
- **Daily**: Monitor performance metrics
- **Weekly**: Review feature distributions
- **Monthly**: Model retraining evaluation
- **Quarterly**: Complete pipeline refresh

## 🚨 Limitations & Considerations

### Current Limitations
- **Geographic Scope**: Limited to USA, UK, Canada locations
- **Merchant Coverage**: Limited to 7 major e-commerce sites
- **Language Support**: English-only text processing
- **Real-time Constraints**: Processing time scales with data size

### Future Enhancements
- **Geographic Expansion**: Support for additional countries
- **Merchant Diversity**: Expand scraping to more sites
- **Multi-language Support**: NLP processing for other languages
- **Deep Learning**: Explore neural network architectures
- **Real-time Streaming**: Kafka integration for live processing

## 📞 Support & Contact

### Technical Support
- **Documentation**: This README file
- **Code Comments**: Comprehensive inline documentation
- **Error Handling**: Robust error messages and logging

### Contributing Guidelines
1. **Code Style**: Follow PEP 8 guidelines
2. **Testing**: Include unit tests for new features
3. **Documentation**: Update README for new functionality
4. **Version Control**: Use semantic versioning

## 📄 License

This project is proprietary and confidential. All rights reserved.

---

## 🚀 Quick Start Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run complete pipeline
python run_all.py

# 3. Launch dashboard
streamlit run interface/app.py

# 4. Upload your transaction data and start detecting fraud!
```

**Expected Performance**: 95.76% accuracy with sub-100ms processing time per transaction.

---

*Last Updated: May 2026*  
*Version: 1.0.0*  
*Maintainer: NexFlow Fraud Detection Team*
