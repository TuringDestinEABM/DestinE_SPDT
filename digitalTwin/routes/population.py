from ..digitaltwin import bp
from flask import render_template, redirect, url_for, flash
from ..library import dataManager, forms, populations

@bp.route('/population', methods=['GET', 'POST'])
def population():
    # 1. Instantiate the form
    popForm = forms.PopulationModelForm()
    
    # 2. Check if the form was submitted and is valid
    if popForm.validate_on_submit():
        # Access data using form.Name.data or form.Wards.data
        print(f"Selected Wards: {popForm.Wards.data}")
        populations.createPopulation(popForm)
        
        # Save to DB here...
        
        return render_template('tempPopulation.html', popForm=popForm)

    # 3. Render the template and pass the form object
    return render_template('tempPopulation.html', popForm=popForm)