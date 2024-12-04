
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'BSH-csv.csv'  # Update the path to your file

# Load the CSV file into a DataFrame
def load_data():
    return pd.read_csv(CSV_FILE)

# Fetch all products
def fetch_products():
    df = load_data()
    return df.to_dict('records')

# Fetch product details and recommendations
def fetch_product_details(product_id):
    df = load_data()

    # Get details of the selected product
    product = df[df['product_id'] == product_id].iloc[0].to_dict()

    # Define pairing rules
    pairing_map = {
        'Washing_machine': ['Dryer', 'tumble_dryer', 'cleaning- WM'],
        'Dryer': ['Washing_machine', 'tumble_dryer', 'cleaning- WM'],
        'tumble_dryer': ['Washing_machine', 'Dryer', 'cleaning- WM'],
        'Oven': ['Microwave', 'Steam_oven', 'glove'],
        'Microwave': ['Oven', 'Steam_oven', 'glove'],
        'Steam_oven': ['Oven', 'Microwave', 'glove'],
        'hob': ['chimney', 'Cooktop', 'Dishwasher'],
        'chimney': ['hob', 'Cooktop', 'Dishwasher'],
        'Cooktop': ['hob', 'chimney', 'Dishwasher'],
        'Dishwasher': ['hob', 'chimney', 'Cooktop'],
        'mixer': ['bleander', 'Food Processor', 'Extractor'],
        'bleander': ['mixer', 'Food Processor', 'Extractor'],
        'Food Processor': ['mixer', 'bleander', 'Extractor'],
        'Extractor': ['mixer', 'bleander', 'Food Processor']
    }

    # Match categories in the pairing map
    selected_category = product.get('category')
    related_categories = pairing_map.get(selected_category, [])

    # Filter recommendations
    recommendations = df[
        (df['category'].isin(related_categories)) &  # Match related categories
        (df['product_id'] != product_id) &           # Exclude selected product
        (df['category'] != selected_category)        # Exclude same category
    ].drop_duplicates(subset='category').head(3).to_dict('records')  # Limit to 3 recommendations

    # Ensure at least 3 recommendations with fallback logic
    if len(recommendations) < 3:
        fallback = df[
            (~df['product_id'].isin([r['product_id'] for r in recommendations])) &  # Exclude current recommendations
            (df['product_id'] != product_id)                                       # Exclude selected product
        ].head(3 - len(recommendations)).to_dict('records')
        recommendations.extend(fallback)

    return product, recommendations

@app.route('/')
def index():
    products = fetch_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product, recommendations = fetch_product_details(product_id)
    return render_template('details.html', product=product, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)






















































#v5
"""
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'BSH-csv.csv'  # Update the path to match your file location

# Load the CSV file into a DataFrame
def load_data():
    return pd.read_csv(CSV_FILE)

# Fetch all products
def fetch_products():
    df = load_data()
    return df.to_dict('records')

# Fetch product details and recommendations
def fetch_product_details(product_id):
    df = load_data()

    # Get details of the selected product
    product = df[df['product_id'] == product_id].iloc[0].to_dict()

    # Define pairing rules (ensure these match your CSV categories exactly)
    pairing_map = {
        'Washing_machine': ['Dryer', 'tumble_dryer', 'cleaning- WM'],
        'Dryer': ['Washing_machine', 'tumble_dryer', 'cleaning- WM'],
        'tumble_dryer': ['Washing_machine', 'Dryer', 'cleaning- WM'],
        'Oven': ['Microwave', 'Steam_oven', 'glove'],
        'Microwave': ['Oven', 'Steam_oven', 'glove'],
        'Steam_oven': ['Oven', 'Microwave', 'glove'],
        'hob': ['chimney', 'Cooktop', 'Dishwasher'],
        'chimney': ['hob', 'Cooktop', 'Dishwasher'],
        'Cooktop': ['hob', 'chimney', 'Dishwasher'],
        'Dishwasher': ['hob', 'chimney', 'Cooktop'],
        'mixer': ['bleander', 'Food Processor', 'Extractor'],
        'bleander': ['mixer', 'Food Processor', 'Extractor'],
        'Food Processor': ['mixer', 'bleander', 'Extractor'],
        'Extractor': ['mixer', 'bleander', 'Food Processor']
    }

    # Ensure selected category exists in the pairing map
    selected_category = product.get('category', None)
    if not selected_category:
        return product, []

    related_categories = pairing_map.get(selected_category, [])

    # Filter recommendations
    recommendations = df[
        (df['category'].isin(related_categories)) &  # Match related categories
        (df['product_id'] != product_id)            # Exclude selected product
    ]

    # Ensure at least 3 unique recommendations
    recommendations = recommendations.drop_duplicates(subset='category').head(3).to_dict('records')
    
    # If fewer than 3, add fallback recommendations
    if len(recommendations) < 3:
        fallback = df[
            (~df['product_id'].isin([r['product_id'] for r in recommendations])) &  # Exclude current recommendations
            (df['product_id'] != product_id)                                       # Exclude selected product
        ].head(4 - len(recommendations)).to_dict('records')
        recommendations.extend(fallback)

    return product, recommendations

@app.route('/')
def index():
    products = fetch_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product, recommendations = fetch_product_details(product_id)
    return render_template('details.html', product=product, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
"""


#v4
"""from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'BSH-csv.csv'  # Update to the path where your file is stored

# Load the CSV file into a DataFrame
def load_data():
    return pd.read_csv(CSV_FILE)

# Fetch all products
def fetch_products():
    df = load_data()
    return df.to_dict('records')

# Fetch product details and recommendations
def fetch_product_details(product_id):
    df = load_data()

    # Get details of the selected product
    product = df[df['product_id'] == product_id].iloc[0].to_dict()

    # Define pairing rules
    pairing_map = {
        'Washing Machine': ['Dryer', 'Tumble Dryer', 'Cleaning-WM'],
        'Dryer': ['Washing Machine', 'Tumble Dryer', 'Cleaning-WM'],
        'Tumble Dryer': ['Washing Machine', 'Dryer', 'Cleaning-WM'],
        'Oven': ['Microwave', 'Steam Ovens', 'Glove'],
        'Microwave': ['Oven', 'Steam Ovens', 'Glove'],
        'Steam Ovens': ['Oven', 'Microwave', 'Glove'],
        'Hob': ['Chimney', 'Cook Top', 'Dishwasher'],
        'Chimney': ['Hob', 'Cook Top', 'Dishwasher'],
        'Cook Top': ['Hob', 'Chimney', 'Dishwasher'],
        'Dishwasher': ['Hob', 'Chimney', 'Cook Top'],
        'Mixer Grinder': ['Blender', 'Food Processor', 'Juice Extractor'],
        'Blender': ['Mixer Grinder', 'Food Processor', 'Juice Extractor'],
        'Food Processor': ['Mixer Grinder', 'Blender', 'Juice Extractor'],
        'Juice Extractor': ['Mixer Grinder', 'Blender', 'Food Processor']
    }

    # Fetch related categories
    related_categories = pairing_map.get(product['category'], [])
    recommendations = df[
        (df['category'].isin(related_categories)) &  # Match related categories
        (df['product_id'] != product_id)            # Exclude selected product
    ]

    # Ensure at least 4 unique recommendations
    recommendations = recommendations.drop_duplicates(subset='category').head(4).to_dict('records')
    
    # If fewer than 4, add fallback recommendations
    if len(recommendations) < 4:
        fallback = df[
            (~df['product_id'].isin([r['product_id'] for r in recommendations])) &  # Exclude current recommendations
            (df['product_id'] != product_id)                                       # Exclude selected product
        ].head(4 - len(recommendations)).to_dict('records')
        recommendations.extend(fallback)

    return product, recommendations

@app.route('/')
def index():
    products = fetch_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product, recommendations = fetch_product_details(product_id)
    return render_template('details.html', product=product, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)


"""










#v3
"""from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'bsh.csv'

# Load the CSV file into a DataFrame
def load_data():
    return pd.read_csv(CSV_FILE)

# Fetch all products
def fetch_products():
    df = load_data()
    return df.to_dict('records')

# Fetch product details and recommendations
def fetch_product_details(product_id):
    df = load_data()

    # Get details of the selected product
    product = df[df['product_id'] == product_id].iloc[0].to_dict()

    # Define recommendation categories
    category_map = {
        'Washing Machine': ['Fridge', 'Dryer'],
        'Refrigerator': ['Washing Machine', 'Dryer'],
        'Oven': ['Microwave', 'Coffee Machine'],
        'Microwave': ['Oven', 'Coffee Machine'],
        'Hobs': ['Chimney', 'Food Processor'],
        'Chimney': ['Hobs', 'Food Processor']
    }

    # Find related products based on category
    related_categories = category_map.get(product['category'], [])
    filtered_df = df[
        (df['category'].isin(related_categories)) &  # Match related categories
        (df['product_id'] != product_id) &           # Exclude selected product
        (df['category'] != product['category'])      # Exclude the same category
    ]

    # Group by category and select one product per category
    recommendations = (
        filtered_df
        .drop_duplicates(subset='category')          # Ensure one product per category
        .head(3)                                     # Limit to 3 unique recommendations
        .to_dict('records')
    )

    return product, recommendations

@app.route('/')
def index():
    products = fetch_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product, recommendations = fetch_product_details(product_id)
    return render_template('details.html', product=product, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)


"""





























#v3


"""from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'bsh.csv'

# Load the CSV file into a DataFrame
def load_data():
    return pd.read_csv(CSV_FILE)

# Fetch all products
def fetch_products():
    df = load_data()
    return df.to_dict('records')

# Fetch product details and recommendations
def fetch_product_details(product_id):
    df = load_data()

    # Get details of the selected product
    product = df[df['product_id'] == product_id].iloc[0].to_dict()

    # Define recommendation categories
    category_map = {
        'Washing Machine': ['Fridge', 'Dryer'],
        'Refrigerator': ['Washing Machine', 'Dryer'],
        'Oven': ['Microwave', 'Coffee Machine'],
        'Microwave': ['Oven', 'Coffee Machine'],
        'Hobs': ['Chimney', 'Food Processor'],
        'Chimney': ['Hobs', 'Food Processor']
    }

    # Find related products based on category
    related_categories = category_map.get(product['category'], [])
    recommendations = (
        df[
            (df['category'].isin(related_categories)) &  # Match related categories
            (df['product_id'] != product_id) &           # Exclude selected product
            (df['category'] != product['category'])      # Exclude the same category
        ]
        .drop_duplicates()
        .head(3)  # Limit to 3 unique recommendations
        .to_dict('records')
    )

    return product, recommendations

@app.route('/')
def index():
    products = fetch_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product, recommendations = fetch_product_details(product_id)
    return render_template('details.html', product=product, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
"""




























#version-2

"""from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'bsh.csv'

# Load the CSV file into a DataFrame
def load_data():
    return pd.read_csv(CSV_FILE)

# Fetch all products
def fetch_products():
    df = load_data()
    return df.to_dict('records')

# Fetch product details and recommendations
def fetch_product_details(product_id):
    df = load_data()

    # Get details of the selected product
    product = df[df['product_id'] == product_id].iloc[0].to_dict()

    # Define recommendation categories
    category_map = {
        'Washing Machine': ['Washing Machine', 'Fridge', 'Dryer'],
        'Refrigerator': ['Washing Machine', 'Fridge', 'Dryer'],
        'Oven': ['Oven', 'Microwave', 'Coffee Machine'],
        'Microwave': ['Oven', 'Microwave', 'Coffee Machine'],
        'Hobs': ['Hobs', 'Chimney', 'Food Processor'],
        'Chimney': ['Hobs', 'Chimney', 'Food Processor']
    }

    # Find related products based on category
    related_categories = category_map.get(product['category'], [])
    recommendations = (
        df[
            (df['category'].isin(related_categories)) & (df['product_id'] != product_id)
        ]
        .drop_duplicates()
        .head(3)  # Limit to 3 unique recommendations
        .to_dict('records')
    )

    return product, recommendations

@app.route('/')
def index():
    products = fetch_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product, recommendations = fetch_product_details(product_id)
    return render_template('details.html', product=product, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
"""














#version-1

"""from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'bsh.csv'

# Load the CSV file into a DataFrame
def load_data():
    return pd.read_csv(CSV_FILE)

# Fetch all products
def fetch_products():
    df = load_data()
    return df.to_dict('records')

# Fetch product details and recommendations
def fetch_product_details(product_id):
    df = load_data()

    # Get details of the selected product
    product = df[df['product_id'] == product_id].iloc[0].to_dict()

    # Define recommendation categories
    category_map = {
        'Washing Machine': ['Washing Machine', 'Fridge', 'Dryer'],
        'Refrigerator': ['Washing Machine', 'Fridge', 'Dryer'],
        'Oven': ['Oven', 'Microwave', 'Coffee Machine'],
        'Microwave': ['Oven', 'Microwave', 'Coffee Machine'],
        'Hobs': ['Hobs', 'Chimney', 'Food Processor'],
        'Chimney': ['Hobs', 'Chimney', 'Food Processor']
    }

    # Find related products based on category
    related_categories = category_map.get(product['category'], [])
    recommendations = df[
        (df['category'].isin(related_categories)) & (df['product_id'] != product_id)
    ].to_dict('records')

    return product, recommendations

@app.route('/')
def index():
    products = fetch_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product, recommendations = fetch_product_details(product_id)
    return render_template('details.html', product=product, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
"""