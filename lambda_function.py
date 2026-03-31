import json
import csv
import boto3
import io
import os
import urllib.parse
from datetime import datetime

s3 = boto3.client("s3")
sns = boto3.client("sns")

def lambda_handler(event, context):
    try:
        sns_topic_arn = os.environ["SNS_TOPIC_ARN"]

        record = event["Records"][0]
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        if not object_key.startswith("input/") or not object_key.endswith(".csv"):
            return {"statusCode": 200, "body": json.dumps("Ignored file")}

        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response["Body"].read().decode("utf-8")

        csv_file = io.StringIO(file_content)
        reader = csv.DictReader(csv_file)

        total_orders = 0
        total_sales = 0.0
        total_quantity_sold = 0

        product_revenue = {}
        category_revenue = {}
        region_revenue = {}
        weekly_analysis = {}

        for row in reader:
            total_orders += 1

            order_date = row["order_date"]
            product = row["product"]
            category = row["category"]
            region = row["region"]
            quantity = float(row["quantity"])
            price = float(row["price"])

            revenue = quantity * price
            total_sales += revenue
            total_quantity_sold += quantity

            product_revenue[product] = product_revenue.get(product, 0) + revenue
            category_revenue[category] = category_revenue.get(category, 0) + revenue
            region_revenue[region] = region_revenue.get(region, 0) + revenue

            parsed_date = datetime.strptime(order_date, "%Y-%m-%d")
            year, week_num, _ = parsed_date.isocalendar()
            week_key = f"{year}-W{week_num:02d}"

            if week_key not in weekly_analysis:
                weekly_analysis[week_key] = {
                    "total_sales": 0.0,
                    "total_orders": 0,
                    "total_quantity_sold": 0
                }

            weekly_analysis[week_key]["total_sales"] += revenue
            weekly_analysis[week_key]["total_orders"] += 1
            weekly_analysis[week_key]["total_quantity_sold"] += quantity

        avg_order = round(total_sales / total_orders, 2)

        report = {
            "total_orders": total_orders,
            "total_sales": round(total_sales, 2),
            "average_order_value": avg_order,
            "total_quantity_sold": int(total_quantity_sold),
            "top_product": max(product_revenue, key=product_revenue.get),
            "top_category": max(category_revenue, key=category_revenue.get),
            "top_region": max(region_revenue, key=region_revenue.get),
            "weekly_analysis": weekly_analysis
        }

        output_key = object_key.replace("input/", "output/").replace(".csv", "_analysis.json")

        s3.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=json.dumps(report, indent=4),
            ContentType="application/json"
        )

        message = f"Sales Analysis Report\nTotal Orders: {total_orders}\nTotal Sales: ${round(total_sales, 2)}\nAverage Order Value: ${avg_order}"

        sns.publish(
            TopicArn=sns_topic_arn,
            Subject="Sales Analysis Report",
            Message=message
        )

        return {"statusCode": 200}

    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
