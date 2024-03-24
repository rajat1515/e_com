from rest_framework import serializers


class CSVValidator:

    @staticmethod
    def validate_csv_data(csv_reader):
        required_fields = ['store', 'name', 'type',
                           'manufacturer', 'price', 'units']

        header_fields = csv_reader.fieldnames
        for field in required_fields:
            if field not in header_fields:
                raise serializers.ValidationError(f"Missing field '{field}'")

        return True
