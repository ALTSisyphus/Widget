import os
from dotenv import load_dotenv
from src.external_api import convert_to_rub

# Загрузка переменных окружения из .env файла
load_dotenv()

# Тестовые транзакции
test_transactions = [
    {
        "operationAmount": {
            "amount": "100",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        }
    },
    {
        "operationAmount": {
            "amount": "50",
            "currency": {
                "name": "EUR",
                "code": "EUR"
            }
        }
    },
    {
        "operationAmount": {
            "amount": "1000",
            "currency": {
                "name": "RUB",
                "code": "RUB"
            }
        }
    }
]


def test_real_conversion():
    print("Testing real currency conversion...")
    print(f"API Key: {'Set' if os.getenv('EXCHANGE_RATES_API_KEY') else 'Not set'}")

    for i, transaction in enumerate(test_transactions, 1):
        result = convert_to_rub(transaction)
        currency = transaction["operationAmount"]["currency"]["code"]
        amount = transaction["operationAmount"]["amount"]

        print(f"Transaction {i}: {amount} {currency} -> {result} RUB")

    print("\nConversion test completed!")


if __name__ == "__main__":
    test_real_conversion()