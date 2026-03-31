from flask import render_template, redirect, url_for, session, request
from ..digitaltwin import bp
from ..library import policies, forms
import time

@bp.route("/create-policy", methods=['GET', 'POST'])
def create_policy():

    policyForm = forms.PolicyChoicesForm(prefix="policy")
    rulesForm = forms.PolicyRulesForm(prefix="rules")

    # Ensure rules list exists in session
    if 'rules' not in session:
        session['rules'] = []

    #  Handle data preservation (Run on every POST)
    if request.method == 'POST':
        session['staged_policy'] = {
            'Name': policyForm.Name.data,
            'Description': policyForm.Description.data
        }
        # Print what button triggered the POST
        # print(f"[DEBUG] POST Action: {request.form.get('btn_action', 'Regular Submit')}")

    action = request.form.get('btn_action', '')
    
    if action == 'delete_all':
        session['rules'] = []
        session.modified = True  
        print("[DEBUG] All rules deleted.")
        return redirect(url_for('digitaltwin.create_policy'))
        
    elif action.startswith('delete_rule_'):
        try:
            rule_id_to_delete = int(action.split('_')[-1])
            existing_rules = session.get('rules', [])
            
            # Filter out the rule
            updated_rules = [r for r in existing_rules if r['temp_id'] != rule_id_to_delete]
            
            session['rules'] = updated_rules
            session.modified = True 
        except ValueError:
            print("[DEBUG] Error parsing rule ID")
            
        return redirect(url_for('digitaltwin.create_policy'))

    # Handle "Add Rule" 
    if rulesForm.Submit.data:  
        if rulesForm.validate():
            new_rule = {
                'temp_id': int(time.time() * 100000), # Unique ID
                'data': rulesForm.data
            }
            
            rules_list = session.get('rules', [])
            rules_list.append(new_rule)
            session['rules'] = rules_list
            session.modified = True 
            
            print(f"[DEBUG] New rule added. ID: {new_rule['temp_id']}")
            return redirect(url_for('digitaltwin.create_policy'))
        else:
            for field, errors in rulesForm.errors.items():
                for error in errors:
                    print('error')
    
    # Handle "Save Policy" 
    if policyForm.Submit.data and policyForm.validate():
        rules = session.get('rules', [])
        
        # Save to DB
        policy_id = policies.savePolicy(policyForm, rules)
        print(f"[DEBUG] Policy Saved! ID: {policy_id}")

        # Cleanup Session
        session.pop('rules', None)
        session.pop('staged_policy', None)
        session.modified = True
        
        return redirect(url_for('digitaltwin.policy_created', id=policy_id))

    # Restore preserved data on page load
    if 'staged_policy' in session:
        if not policyForm.Name.data:
            policyForm.Name.data = session['staged_policy'].get('Name')
        if not policyForm.Description.data:
            policyForm.Description.data = session['staged_policy'].get('Description')

    return render_template("policies.html", 
                           policyForm=policyForm,
                           rulesForm=rulesForm)

@bp.route("/policy-created/<id>")
def policy_created(id):
    return render_template("policy_created.html", 
                           id=id)