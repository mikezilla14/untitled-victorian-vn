import sys
import yaml
import argparse
import fnmatch

def load_guardrails(yaml_path):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def check_permission(agent, files_changed, guardrails):
    violations = []
    
    for file in files_changed:
        allowed = False
        # Check against every domain in .guardrails.yml
        for domain_name, domain_data in guardrails.get('domains', {}).items():
            for path_pattern in domain_data.get('paths', []):
                # If the changed file matches a protected path pattern
                if fnmatch.fnmatch(file, path_pattern):
                    if agent in domain_data.get('mutable_by', []) or 'all' in domain_data.get('mutable_by', []):
                        allowed = True
                    break
            if allowed:
                break
                
        if not allowed:
            violations.append(file)
            
    return violations

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True, help="Name of the agent making the PR")
    parser.add_argument("--files", required=True, help="Comma separated list of files changed")
    args = parser.parse_args()

    files_list = [f.strip() for f in args.files.split(',') if f.strip()]
    guardrails = load_guardrails('.guardrails.yml')

    print(f"🛡️ Gatekeeper Orchestrator checking permissions for '{args.agent}'...")
    
    violations = check_permission(args.agent, files_list, guardrails)
    
    if violations:
        print(f"❌ SECURITY ALERT: Agent '{args.agent}' is not authorized to modify:")
        for v in violations:
            print(f"   - {v}")
        print("Merge rejected. Human override required.")
        sys.exit(1)
    else:
        print("✅ All file modifications are within authorized domains.")
        sys.exit(0)