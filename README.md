# 🚀 AWS Serverless Sales Data Analysis Pipeline

An end-to-end serverless data analysis pipeline that automatically processes sales CSV data, generates business KPIs (including weekly insights), and delivers results via email using AWS services.

---

## 📌 Project Overview

This project demonstrates how to build a real-world data pipeline using AWS serverless services.

Whenever a CSV file is uploaded to Amazon S3, the system:
- Automatically processes the data  
- Generates key business insights  
- Stores results in structured JSON format  
- Sends a notification email  

---

## 🏗️ Architecture
User Upload → S3 (input/)
↓
AWS Lambda Trigger
↓
Data Processing & Analysis
↓
S3 (output/) JSON Report
↓
SNS Email Notification


---

## ⚙️ Features

- 📥 Upload CSV → automatic processing  
- ⚡ Event-driven architecture using S3 triggers  
- 📊 KPI calculations:
  - Total Orders  
  - Total Sales  
  - Average Order Value  
  - Total Quantity Sold  
- 🏆 Top performers:
  - Product  
  - Category  
  - Region  
- 📅 Weekly sales analysis  
- 📁 JSON output report stored in S3  
- 📧 Email notification via SNS  

---

## 🧠 Data Analysis Performed

The Lambda function performs:

- Sales aggregation and KPI computation  
- Revenue analysis by product, category, and region  
- Weekly trend analysis using date grouping  
- Business insights generation  

---

## 📂 Project Structure
aws-sales-data-analysis/
├── lambda_function.py
├── README.md
├── sample-data/
│ └── sales.csv

<img width="1362" height="435" alt="image" src="https://github.com/user-attachments/assets/28542222-32ce-4fd9-9d70-303783dc7e5a" />
<img width="884" height="521" alt="image" src="https://github.com/user-attachments/assets/f829d593-8647-4582-b4eb-0dcf10122b3d" />
<img width="540" height="554" alt="image" src="https://github.com/user-attachments/assets/7f306795-89e8-4946-8f41-0444871833f1" />



---

## 📄 Sample Input

```csv
order_id,order_date,product,category,region,quantity,price
1,2026-03-01,Laptop,Electronics,East,1,800
2,2026-03-02,Mouse,Electronics,West,2,25
3,2026-03-05,Chair,Furniture,South,1,120

![Uploading image.png…]()
