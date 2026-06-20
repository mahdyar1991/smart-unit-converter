from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')  # Matches your 'template' folder name

CONVERSIONS = {
    "mass": {
        "base": "g",
        "rates": {"g": 1.0, "kg": 1000.0, "lb": 453.59237}
    },
    "length": {
        "base": "m",
        "rates": {"m": 1.0, "cm": 0.01, "inch": 0.0254, "feet": 0.3048, "km": 1000.0} # Fixed 'kn' typo to 'km'
    },
    "pressure": {
        "base": "atm",
        "rates": {"atm": 1.0, "bar": 0.986923, "psi": 0.068046, "cmHg": 0.0131579}
    },
    "time": {
        "base": "s",
        "rates": {"s": 1.0, "min": 60.0, "h": 3600.0, "day": 86400.0}
    }
}

def convert_units(category, value, from_unit, to_unit):
    if category == "temp":
        if from_unit == "C": k = value + 273.15
        elif from_unit == "F": k = (value - 32) * 5/9 + 273.15
        elif from_unit == "R": k = value * 5/9
        else: k = value
        
        if to_unit == "C": return k - 273.15
        elif to_unit == "F": return (k - 273.15) * 9/5 + 32
        elif to_unit == "R": return k * 9/5
        return k

    config = CONVERSIONS.get(category)
    if not config:
        return None
    
    # Convert to base unit, then convert to target unit
    value_in_base = value * config["rates"][from_unit]
    return value_in_base / config["rates"][to_unit]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected_category = "mass"
    from_unit = ""
    to_unit = ""
    val = ""

    if request.method == "POST":
        selected_category = request.form.get("category")
        from_unit = request.form.get("from_unit")
        to_unit = request.form.get("to_unit")
        val = request.form.get("value")
        
        if val:
            try:
                res_val = convert_units(selected_category, float(val), from_unit, to_unit)
                result = f"{val} {from_unit} = {res_val:.4f} {to_unit}"
            except ValueError:
                result = "Invalid input value."

    # Send categories and their units to the template to dynamically build dropdowns
    categories = {
        "mass": ["g", "kg", "lb"],
        "length": ["inch", "cm", "feet", "m", "km"],
        "temp": ["C", "F", "K", "R"],
        "pressure": ["atm", "bar", "psi", "cmHg"],
        "time": ["s", "min", "h", "day"]
    }

    return render_template("index.html", categories=categories, result=result, 
                           selected_category=selected_category, from_unit=from_unit, to_unit=to_unit, val=val)

if __name__ == "__main__":
    app.run(debug=True)