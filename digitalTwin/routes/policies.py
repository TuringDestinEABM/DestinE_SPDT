from flask import render_template, redirect, url_for, session, request, flash
from ..digitaltwin import bp
from ..library import policies, forms
import time

@bp.route("/create-policy", methods=['GET', 'POST'])
def create_policy():
    
    # session cleanup on arrival
    # make sure to include the flag new=1 in url_for()
    if request.method == 'GET':
        is_new_link = request.args.get('new') == '1'
        is_direct_typing = request.referrer is None

        if is_new_link or is_direct_typing:
            session.pop('rules', None)
            session.pop('staged_policy', None)
            session.modified = True
            
            if is_new_link:
                return redirect(url_for('digitaltwin.create_policy'))
    # get wtforms
    policyForm = forms.PolicyChoicesForm(prefix="policy")
    rulesForm = forms.PolicyRulesForm(prefix="rules")

    if 'rules' not in session:
        session['rules'] = []

    if request.method == 'POST':
        session['staged_policy'] = {
            'Name': policyForm.Name.data,
            'Description': policyForm.Description.data
        }

    action = request.form.get('btn_action', '')
    
    # delete logic
    if action == 'delete_all':
        session['rules'] = []
        session.modified = True  
        return redirect(url_for('digitaltwin.create_policy'))
        
    elif action.startswith('delete_rule_'):
        try:
            rule_id_to_delete = int(action.split('_')[-1])
            existing_rules = session.get('rules', [])
            
            updated_rules = [r for r in existing_rules if r['temp_id'] != rule_id_to_delete]
            
            session['rules'] = updated_rules
            session.modified = True 
        except ValueError:
            pass
            
        return redirect(url_for('digitaltwin.create_policy'))

    # submit logic (rules)
    if rulesForm.Submit.data:  
        if rulesForm.validate():
            new_rule = {
                'temp_id': int(time.time() * 100000), 
                'data': rulesForm.data
            }
            
            rules_list = session.get('rules', [])
            rules_list.append(new_rule)
            session['rules'] = rules_list
            session.modified = True 
            
            return redirect(url_for('digitaltwin.create_policy'))
    
    # submit logic (policy)
    if policyForm.Submit.data:
        rules = session.get('rules', [])
        
        if not rules:
            flash('You must add at least one rule to the policy before saving.', 'danger')
        elif policyForm.validate():
            policy_id = policies.savePolicy(policyForm, rules)

            session.pop('rules', None)
            session.pop('staged_policy', None)
            session.modified = True
            
            return redirect(url_for('digitaltwin.policy_created', id=policy_id))

    # staged policy logic
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
    policy_data = policies.getPolicy(id)
    return render_template("policy_created.html",
                           policy_data=policy_data,
                           id=id)