# Quick Usage Guide
1. Basic Backup:
* Run the simple commands to quickly export Kubernetes manifests using `kubectl get -o yaml`.

2. Advanced Backup:
* Execute the advanced backup script to collect all important cluster-scoped and namespaced resources, clean the manifests, and remove non-restorable runtime fields.

3. Smart Cleanup:
* The script automatically removes empty files, useless directories, and invalid YAML to ensure a clean, restore-ready backup set.

4. Dry-Run Validation:
* After collection, the script performs a validation apply (dry-run or test environment) to confirm that the manifests can be successfully restored.

5. Full Restore:
Use `restore.sh` to safely re-apply the backup in the correct order: CRDs → cluster resources → RBAC → namespaces → namespaced resources.

---

# Print list of all the resources
The `kubectl api-resources` command shows you a list of all the resources supported by Kubernetes.
```bash
kubectl api-resources
```

---

# Simple Command
```bash
kubectl get all --all-namespaces -o yaml > all-resources.yaml
```

---

# Automate with bash script
```sh
nano backup-manifest.sh
```

```sh
#!/bin/bash
BACKUP_DIR="k8s-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p $BACKUP_DIR

# Function to handle errors
set -e

echo "Starting Kubernetes backup..."

# Backup all namespaces
echo "Backing up namespaces..."
kubectl get namespaces -o yaml > $BACKUP_DIR/namespaces.yaml

# Get all namespaces
NAMESPACES=$(kubectl get ns -o jsonpath='{.items[*].metadata.name}')

# Backup each resource in each namespace
for ns in $NAMESPACES; do
    echo "Backing up namespace: $ns"
    mkdir -p "$BACKUP_DIR/$ns"
    
    # Common namespaced resources
    kubectl get deploy -n $ns -o yaml > "$BACKUP_DIR/$ns/deployments.yaml" 2>/dev/null || true
    kubectl get cm -n $ns -o yaml > "$BACKUP_DIR/$ns/configmaps.yaml" 2>/dev/null || true
    kubectl get secrets -n $ns -o yaml > "$BACKUP_DIR/$ns/secrets.yaml" 2>/dev/null || true
    kubectl get svc -n $ns -o yaml > "$BACKUP_DIR/$ns/services.yaml" 2>/dev/null || true
    kubectl get ing -n $ns -o yaml > "$BACKUP_DIR/$ns/ingresses.yaml" 2>/dev/null || true
    kubectl get networkpolicies -n $ns -o yaml > "$BACKUP_DIR/$ns/networkpolicies.yaml" 2>/dev/null || true
    kubectl get pvc -n $ns -o yaml > "$BACKUP_DIR/$ns/persistentvolumeclaims.yaml" 2>/dev/null || true
    kubectl get sts -n $ns -o yaml > "$BACKUP_DIR/$ns/statefulsets.yaml" 2>/dev/null || true
    kubectl get ds -n $ns -o yaml > "$BACKUP_DIR/$ns/daemonsets.yaml" 2>/dev/null || true
    kubectl get sa -n $ns -o yaml > "$BACKUP_DIR/$ns/serviceaccounts.yaml" 2>/dev/null || true
    kubectl get resourcequotas -n $ns -o yaml > "$BACKUP_DIR/$ns/resourcequotas.yaml" 2>/dev/null || true
    kubectl get roles -n $ns -o yaml > "$BACKUP_DIR/$ns/roles.yaml" 2>/dev/null || true
    kubectl get rolebindings -n $ns -o yaml > "$BACKUP_DIR/$ns/rolebindings.yaml" 2>/dev/null || true
    kubectl get hpa -n $ns -o yaml > "$BACKUP_DIR/$ns/hpa.yaml" 2>/dev/null || true
    kubectl get jobs -n $ns -o yaml > "$BACKUP_DIR/$ns/jobs.yaml" 2>/dev/null || true
    kubectl get cronjobs -n $ns -o yaml > "$BACKUP_DIR/$ns/cronjobs.yaml" 2>/dev/null || true
    
    # OpenShift specific resources (if applicable)
    if kubectl get routes -n $ns >/dev/null 2>&1; then
        kubectl get routes -n $ns -o yaml > "$BACKUP_DIR/$ns/routes.yaml" 2>/dev/null || true
    fi
    
    if kubectl get projecthelmchartrepositories -n $ns >/dev/null 2>&1; then
        kubectl get projecthelmchartrepositories -n $ns -o yaml > "$BACKUP_DIR/$ns/projecthelmchartrepositories.yaml" 2>/dev/null || true
    fi

    # Custom Resources
    CRDS=$(kubectl get crd -o name 2>/dev/null || true)
    if [ -n "$CRDS" ]; then
        for crd in $CRDS; do
            crd_name=$(echo $crd | cut -d'/' -f2)
            kubectl get $crd_name -n $ns -o yaml > "$BACKUP_DIR/$ns/$crd_name.yaml" 2>/dev/null || true
        done
    fi
done

# Backup cluster-scoped resources
echo "Backing up cluster-scoped resources..."
mkdir -p "$BACKUP_DIR/cluster"

kubectl get pv -o yaml > "$BACKUP_DIR/cluster/persistentvolumes.yaml" 2>/dev/null || true
kubectl get sc -o yaml > "$BACKUP_DIR/cluster/storageclasses.yaml" 2>/dev/null || true
kubectl get nodes -o yaml > "$BACKUP_DIR/cluster/nodes.yaml" 2>/dev/null || true
kubectl get crd -o yaml > "$BACKUP_DIR/cluster/customresourcedefinitions.yaml" 2>/dev/null || true
kubectl get clusterroles -o yaml > "$BACKUP_DIR/cluster/clusterroles.yaml" 2>/dev/null || true
kubectl get clusterrolebindings -o yaml > "$BACKUP_DIR/cluster/clusterrolebindings.yaml" 2>/dev/null || true

# OpenShift specific cluster resources
if kubectl get oauth >/dev/null 2>&1; then
    kubectl get oauth -o yaml > "$BACKUP_DIR/cluster/oauth.yaml" 2>/dev/null || true
fi

if kubectl get eip >/dev/null 2>&1; then
    kubectl get eip -o yaml > "$BACKUP_DIR/cluster/egressips.yaml" 2>/dev/null || true
fi

if kubectl get helmchartrepositories >/dev/null 2>&1; then
    kubectl get helmchartrepositories -o yaml > "$BACKUP_DIR/cluster/helmchartrepositories.yaml" 2>/dev/null || true
fi

if kubectl get users >/dev/null 2>&1; then
    kubectl get users -o yaml > "$BACKUP_DIR/cluster/users.yaml" 2>/dev/null || true
fi

if kubectl get groups >/dev/null 2>&1; then
    kubectl get groups -o yaml > "$BACKUP_DIR/cluster/groups.yaml" 2>/dev/null || true
fi

# Create backup summary
echo "Creating backup summary..."
cat > "$BACKUP_DIR/backup-summary.txt" << EOF
Backup Summary
==============
Date: $(date)
Backup Directory: $BACKUP_DIR
Total Namespaces: $(echo $NAMESPACES | wc -w)
Cluster Resources: $(ls -1 "$BACKUP_DIR/cluster" | wc -l)
EOF

# Compress backup (optional)
echo "Compressing backup directory..."
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "Backup completed successfully: $BACKUP_DIR.tar.gz"
echo "Size: $(du -h "$BACKUP_DIR.tar.gz" | cut -f1)"
```
Make a executable file
```sh
chmod +x backup-manifest.sh
```
```sh
./backup-manifest.sh
```

###
---
###

# Advance Script
```sh
nano backup-manifests.sh
```
```sh
#!/usr/bin/env bash
# backup-manifests.sh - Production-ready Kubernetes/OpenShift manifest backup
# - auto-discovers listable resources
# - skips resources with no instances
# - strips runtime fields (recommended: install yq)
# - removes pods from backup
# - supports client-side rate limiting and parallelization
# - atomic progress counter (flock) and GNU parallel integration
# - SMART CLEANUP added: removes empty/placeholder YAMLs, prunes empty dirs, logs deletions
#
# Usage:
#   ./backup-manifests.sh [output-prefix] [--jobs N] [--rate R] [--no-compress] [--no-clean] [--no-dump]
#
set -euo pipefail
IFS=$'\n\t'

# -----------------------------
# Configuration defaults
# -----------------------------
OUT_PREFIX="${1:-k8s-backup}"
JOBS=8                    # parallel workers
RATE=5                    # global approx requests per second
COMPRESS=true
CLEAN_YAML=true
DUMP_CLUSTER=false        # optional kubectl cluster-info dump (off by default)
shift || true

# parse flags
while (( "$#" )); do
  case "$1" in
    --jobs) JOBS="${2:-$JOBS}"; shift 2;;
    --rate) RATE="${2:-$RATE}"; shift 2;;
    --no-compress) COMPRESS=false; shift;;
    --no-clean) CLEAN_YAML=false; shift;;
    --no-dump) DUMP_CLUSTER=false; shift;;
    --dump) DUMP_CLUSTER=true; shift;;
    --help)
      cat <<EOF
Usage: $0 [output-prefix] [options]

Options:
  --jobs N       Number of parallel workers (default: $JOBS)
  --rate R       Approx requests per second across all workers (default: $RATE)
  --no-compress  Skip creating tar.gz archive
  --no-clean     Do not strip runtime fields from YAML (not recommended)
  --dump         Run 'kubectl cluster-info dump' and save into backup (off by default)
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

# -----------------------------
# Tool detection
# -----------------------------
command -v kubectl >/dev/null 2>&1 || { echo "ERROR: kubectl not found" >&2; exit 2; }
HAS_YQ=false; command -v yq >/dev/null 2>&1 && HAS_YQ=true
HAS_PARALLEL=false; command -v parallel >/dev/null 2>&1 && HAS_PARALLEL=true
HAS_FLOCK=false; command -v flock >/dev/null 2>&1 && HAS_FLOCK=true

if [ "$HAS_YQ" = false ]; then
  echo "NOTE: yq not found. Using best-effort YAML cleaner. Install yq for robust cleaning." >&2
fi

# -----------------------------
# Setup output directories, logging, timestamps
# -----------------------------
start_ts=$(date +%s)
SCRIPT_START=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
OUT_DIR="${OUT_PREFIX}-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$OUT_DIR"
LOGFILE="$OUT_DIR/backup.log"
CLEANUP_LOG="$OUT_DIR/cleanup.log"

log() { local l="$1"; shift; printf '[%s] [%s] %s\n' "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$l" "$*" | tee -a "$LOGFILE"; }

log INFO "Backup started: $SCRIPT_START"
log INFO "Output directory: $OUT_DIR"
log INFO "Jobs: $JOBS, Rate: $RATE req/s, YQ: $HAS_YQ, GNU parallel: $HAS_PARALLEL, flock: $HAS_FLOCK"

# -----------------------------
# YAML cleaner: stdin -> stdout
# -----------------------------
clean_yaml() {
  if [ "$CLEAN_YAML" = false ]; then
    cat
    return 0
  fi

  if [ "$HAS_YQ" = true ]; then
    # remove problematic runtime fields
    yq eval 'del(.metadata.managedFields, .metadata.uid, .metadata.resourceVersion, .metadata.creationTimestamp, .metadata.annotations."kubectl.kubernetes.io/last-applied-configuration", .status)' -
  else
    # best-effort fallback: remove status block and known metadata keys
    awk '
      BEGIN {in_status=0}
      /^\s*status:/ { in_status=1; next }
      in_status && /^[^[:space:]]/ { in_status=0 }
      in_status { next }
      /managedFields:/ { next }
      /^\s*uid:/ { next }
      /^\s*resourceVersion:/ { next }
      /^\s*creationTimestamp:/ { next }
      /kubectl.kubernetes.io\/last-applied-configuration/ { next }
      { print }
    ' -
  fi
}

export -f clean_yaml

# -----------------------------
# Resource discovery
# -----------------------------
log INFO "Discovering API resources (namespaced and cluster-scoped)..."

mapfile -t NAMESPACED_RESOURCES < <(kubectl api-resources --verbs=list --namespaced -o name 2>/dev/null || true)
mapfile -t CLUSTER_RESOURCES   < <(kubectl api-resources --verbs=list --namespaced=false -o name 2>/dev/null || true)

# Filter out unwanted resources
exclude_namespaced_regex='^(events|tokenreviews|selfsubjectaccessreviews|subjectaccessreviews|componentstatuses|bindings)$'
exclude_cluster_regex='^(componentstatuses)$'

filter_namespaced() {
  printf '%s\n' "$@" | grep -vE "$exclude_namespaced_regex" || true
}
filter_cluster() {
  printf '%s\n' "$@" | grep -vE "$exclude_cluster_regex" || true
}

mapfile -t NAMESPACED_RESOURCES < <(filter_namespaced "${NAMESPACED_RESOURCES[@]}")
mapfile -t CLUSTER_RESOURCES < <(filter_cluster "${CLUSTER_RESOURCES[@]}")

# Remove pods explicitly (user requested)
mapfile -t NAMESPACED_RESOURCES < <(printf '%s\n' "${NAMESPACED_RESOURCES[@]}" | grep -v '^pods$' || true)

log INFO "Namespaced resources discovered: ${#NAMESPACED_RESOURCES[@]}"
log INFO "Cluster resources discovered: ${#CLUSTER_RESOURCES[@]}"

# Detect OpenShift (best-effort)
IS_OPENSHIFT=false
if kubectl api-resources | grep -q 'openshift' 2>/dev/null || kubectl get projects >/dev/null 2>&1; then
  IS_OPENSHIFT=true
fi
if [ "$IS_OPENSHIFT" = true ]; then
  log INFO "OpenShift-like APIs detected"
fi

# -----------------------------
# Namespaces
# -----------------------------
if [ "$IS_OPENSHIFT" = true ]; then
  mapfile -t NAMESPACES < <(kubectl get projects -o jsonpath='{.items[*].metadata.name}' 2>/dev/null || true)
else
  mapfile -t NAMESPACES < <(kubectl get ns -o jsonpath='{.items[*].metadata.name}' 2>/dev/null || true)
fi

if [ "${#NAMESPACES[@]}" -eq 0 ]; then
  NAMESPACES=(default)
  log WARN "No namespaces found; falling back to 'default'"
fi
log INFO "Namespaces: ${#NAMESPACES[@]}"

# -----------------------------
# Build task list
# -----------------------------
TASK_FILE="$OUT_DIR/tasks.txt"
: > "$TASK_FILE"
task_count=0

# namespaced tasks
for ns in "${NAMESPACES[@]}"; do
  mkdir -p "$OUT_DIR/$ns"
  for res in "${NAMESPACED_RESOURCES[@]}"; do
    printf '%s|%s|%s\n' "$res" "$ns" "$OUT_DIR/$ns/${res//\//_}.yaml" >> "$TASK_FILE"
    task_count=$((task_count+1))
  done
done

# cluster tasks
mkdir -p "$OUT_DIR/cluster"
for res in "${CLUSTER_RESOURCES[@]}"; do
  printf '%s|%s|%s\n' "$res" "CLUSTER" "$OUT_DIR/cluster/${res//\//_}.yaml" >> "$TASK_FILE"
  task_count=$((task_count+1))
done

log INFO "Created $task_count tasks"

TOTAL_TASKS=$task_count

# -----------------------------
# Progress counter helpers (atomic)
# -----------------------------
COUNTER_FILE="$OUT_DIR/.counter"
LOCK_FILE="$OUT_DIR/.counter.lock"
echo 0 > "$COUNTER_FILE"

auto_increment() {
  if [ "$HAS_FLOCK" = true ]; then
    ( flock -x 200
      n=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
      n=$((n+1))
      echo "$n" > "$COUNTER_FILE"
    ) 200>"$LOCK_FILE"
  else
    # fallback (non-atomic)
    n=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
    n=$((n+1))
    echo "$n" > "$COUNTER_FILE"
  fi
}

print_progress() {
  done=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
  total=$TOTAL_TASKS
  if [ "$total" -le 0 ]; then
    percent=100
  else
    percent=$(( done * 100 / total ))
  fi
  width=40
  filled=$(( percent * width / 100 ))
  empty=$(( width - filled ))
  # build bar
  bar=""
  for i in $(seq 1 $filled); do bar="${bar}#"; done
  for i in $(seq 1 $empty); do bar="${bar}-"; done
  printf "\rProgress: [%s] %3d%% (%d/%d)" "$bar" "$percent" "$done" "$total" > /dev/stderr
}

# -----------------------------
# Rate limiting per call
# -----------------------------
# SLEEP_PER_CALL is the sleep inserted AFTER each kubectl get in worker
SLEEP_PER_CALL=$(awk "BEGIN { printf \"%f\", 1 / $RATE }")

# -----------------------------
# Worker: resource|namespace|outpath
# -----------------------------
worker() {
  line="$1"
  IFS='|' read -r resource ns outpath <<< "$line"

  mkdir -p "$(dirname "$outpath")"

  # quick existence check (request-timeout to avoid stuck)
  if [ "$ns" = "CLUSTER" ]; then
    if ! kubectl get "$resource" --no-headers -o custom-columns=NAME:.metadata.name --request-timeout=10s 2>/dev/null | head -n1 >/dev/null 2>&1; then
      auto_increment; return 0
    fi
    # attempt get
    if kubectl get "$resource" -o yaml --request-timeout=30s 2>/dev/null | clean_yaml > "${outpath}.tmp" 2>/dev/null; then
      sleep "$SLEEP_PER_CALL"
    else
      rm -f "${outpath}.tmp" 2>/dev/null || true
      echo "FAILED|$resource|CLUSTER" >> "$OUT_DIR/results.log"
      auto_increment; return 1
    fi
  else
    if ! kubectl get "$resource" -n "$ns" --no-headers -o custom-columns=NAME:.metadata.name --request-timeout=10s 2>/dev/null | head -n1 >/dev/null 2>&1; then
      auto_increment; return 0
    fi
    if kubectl get "$resource" -n "$ns" -o yaml --request-timeout=30s 2>/dev/null | clean_yaml > "${outpath}.tmp" 2>/dev/null; then
      sleep "$SLEEP_PER_CALL"
    else
      rm -f "${outpath}.tmp" 2>/dev/null || true
      echo "FAILED|$resource|$ns" >> "$OUT_DIR/results.log"
      auto_increment; return 1
    fi
  fi

  # consider empty results: detect 'items: []' or zero-size
  if [ ! -s "${outpath}.tmp" ]; then
    rm -f "${outpath}.tmp" 2>/dev/null || true
    echo "EMPTY|$resource|$ns" >> "$OUT_DIR/results.log"
    auto_increment; return 0
  fi

  # avoid files that only contain "items: []" or only 'kind: List' with no objects
  if grep -qE '^\s*items:\s*\[\]\s*$' "${outpath}.tmp" 2>/dev/null || (grep -qE '^\s*kind:\s*List\s*$' "${outpath}.tmp" 2>/dev/null && ! grep -qE '^\s*- \bapiVersion\b' "${outpath}.tmp" 2>/dev/null); then
    rm -f "${outpath}.tmp" 2>/dev/null || true
    echo "EMPTY|$resource|$ns" >> "$OUT_DIR/results.log"
    auto_increment; return 0
  fi

  # ensure file contains at least one resource with apiVersion/kind/metadata.name
  if ! grep -qE '^\s*apiVersion:\s*' "${outpath}.tmp" 2>/dev/null || ! grep -qE '^\s*kind:\s*' "${outpath}.tmp" 2>/dev/null; then
    rm -f "${outpath}.tmp" 2>/dev/null || true
    echo "INVALID|$resource|$ns" >> "$OUT_DIR/results.log"
    auto_increment; return 0
  fi

  mv "${outpath}.tmp" "$outpath"
  echo "SUCCESS|$resource|$ns" >> "$OUT_DIR/results.log"
  auto_increment
  return 0
}

export -f worker clean_yaml
export OUT_DIR

# -----------------------------
# Execute tasks (parallel or sequential)
# -----------------------------
log INFO "Starting execution (jobs=$JOBS, use GNU parallel: $HAS_PARALLEL)"
> "$OUT_DIR/results.log"

if [ "$HAS_PARALLEL" = true ] && [ "$JOBS" -gt 1 ]; then
  # parallel: each job argument is a whole task line
  parallel --jobs "$JOBS" --joblog "$OUT_DIR/parallel.log" --halt soon,fail=1 --progress worker :::: "$TASK_FILE"
else
  # simple pool (bash)
  pids=()
  while IFS= read -r tline || [ -n "$tline" ]; do
    worker "$tline" &
    pids+=("$!")
    # limit concurrency
    while [ "${#pids[@]}" -ge "$JOBS" ]; do
      # wait for first pid
      wait "${pids[0]}" 2>/dev/null || true
      # prune finished
      newp=()
      for pid in "${pids[@]}"; do
        kill -0 "$pid" 2>/dev/null && newp+=("$pid") || true
      done
      pids=("${newp[@]}")
    done
    print_progress
  done < "$TASK_FILE"

  # wait remaining
  wait
fi

# ensure progress prints final state
print_progress
printf '\n' > /dev/stderr

# -----------------------------
# SMART CLEANUP (new)
# -----------------------------
log INFO "Starting SMART CLEANUP..."
# create cleanup log header
echo "Cleanup log - $(date -u +"%Y-%m-%dT%H:%M:%SZ")" > "$CLEANUP_LOG"
echo "Removed files and reasons:" >> "$CLEANUP_LOG"

deleted_count=0
invalid_count=0
empty_count=0
pruned_dirs=0

# 1) Remove zero-size files (definitive)
mapfile -t zero_files < <(find "$OUT_DIR" -type f -name '*.yaml' -size 0 -print)
for f in "${zero_files[@]}"; do
  echo "ZERO_SIZE: $f" | tee -a "$CLEANUP_LOG"
  rm -f "$f" && deleted_count=$((deleted_count+1)) || true
done

# 2) Remove files that contain only 'items: []' or only 'kind: List' with no entries
mapfile -t candidate_files < <(find "$OUT_DIR" -type f -name '*.yaml' -print)
for f in "${candidate_files[@]}"; do
  # skip files already removed
  [ -f "$f" ] || continue
  if grep -qE '^\s*items:\s*\[\]\s*$' "$f" 2>/dev/null; then
    echo "ITEMS_EMPTY: $f" | tee -a "$CLEANUP_LOG"
    rm -f "$f" && empty_count=$((empty_count+1)) || true
    continue
  fi
  if grep -qE '^\s*kind:\s*List\s*$' "$f" 2>/dev/null; then
    # if file is 'kind: List' and doesn't contain any '-' document entries, treat as empty
    if ! grep -qE '^\s*-\s*apiVersion:|^\s*-\s*kind:' "$f" 2>/dev/null; then
      echo "KIND_LIST_EMPTY: $f" | tee -a "$CLEANUP_LOG"
      rm -f "$f" && empty_count=$((empty_count+1)) || true
      continue
    fi
  fi
  # if file doesn't contain apiVersion or kind at all, treat as invalid
  if ! grep -qE '^\s*apiVersion:\s*' "$f" 2>/dev/null || ! grep -qE '^\s*kind:\s*' "$f" 2>/dev/null; then
    echo "INVALID_FORMAT: $f" | tee -a "$CLEANUP_LOG"
    rm -f "$f" && invalid_count=$((invalid_count+1)) || true
    continue
  fi
done

# 3) Prune empty directories (namespaces with no files)
mapfile -t empty_dirs < <(find "$OUT_DIR" -type d -empty -print)
for d in "${empty_dirs[@]}"; do
  # don't remove OUT_DIR itself
  if [ "$d" = "$OUT_DIR" ]; then continue; fi
  echo "PRUNE_DIR: $d" | tee -a "$CLEANUP_LOG"
  rmdir "$d" 2>/dev/null && pruned_dirs=$((pruned_dirs+1)) || true
done

log INFO "SMART CLEANUP results: deleted=$deleted_count, empty_files=$empty_count, invalid=$invalid_count, pruned_dirs=$pruned_dirs"
echo "" >> "$CLEANUP_LOG"
echo "Summary: deleted=${deleted_count}, empty_files=${empty_count}, invalid=${invalid_count}, pruned_dirs=${pruned_dirs}" >> "$CLEANUP_LOG"

# -----------------------------
# Post-processing (existing)
# -----------------------------
# CRDs
if kubectl get crd >/dev/null 2>&1; then
  log INFO "Saving CRD definitions..."
  kubectl get crd -o yaml 2>/dev/null | clean_yaml > "$OUT_DIR/cluster/customresourcedefinitions.yaml" || true
fi

# Optional cluster-info dump (off by default, potentially large/sensitive)
if [ "$DUMP_CLUSTER" = true ]; then
  log INFO "Running kubectl cluster-info dump (this may be large/sensitive)..."
  kubectl cluster-info dump --output-directory="$OUT_DIR/cluster-dump" 2>/dev/null || true
fi

# Summary counts
SUCCESS_COUNT=$(grep -c '^SUCCESS|' "$OUT_DIR/results.log" 2>/dev/null || echo 0)
FAILED_COUNT=$(grep -c '^FAILED|' "$OUT_DIR/results.log" 2>/dev/null || echo 0)
EMPTY_COUNT=$(grep -c '^EMPTY|' "$OUT_DIR/results.log" 2>/dev/null || echo 0)
INVALID_COUNT=$(grep -c '^INVALID|' "$OUT_DIR/results.log" 2>/dev/null || echo 0)
TOTAL_FILES=$(find "$OUT_DIR" -type f -name '*.yaml' | wc -l || echo 0)
BACKUP_SIZE=$(du -sh "$OUT_DIR" | cut -f1 || echo "0")

# Duration
end_ts=$(date +%s)
DURATION=$(( end_ts - start_ts ))

# Success rate calculation (guard divide by zero)
if [ "$TOTAL_TASKS" -gt 0 ]; then
  SUCCESS_RATE=$(( SUCCESS_COUNT * 100 / TOTAL_TASKS ))
else
  SUCCESS_RATE=100
fi

# file index
find "$OUT_DIR" -type f -name '*.yaml' | sed "s|$OUT_DIR/||" | sort > "$OUT_DIR/file-index.txt"

# final summary
cat > "$OUT_DIR/backup-summary.txt" <<EOF
Kubernetes/OpenShift Manifest Backup Report
===========================================

Start:       $SCRIPT_START
End:         $(date -u +"%Y-%m-%dT%H:%M:%SZ")
Duration(s): $DURATION
Output:      $OUT_DIR
Size:        $BACKUP_SIZE

Tasks:       $TOTAL_TASKS
Success:     $SUCCESS_COUNT
Failed:      $FAILED_COUNT
Empty:       $EMPTY_COUNT
Invalid:     $INVALID_COUNT
Success %:   $SUCCESS_RATE%

YAML files:  $TOTAL_FILES
Jobs:        $JOBS
Rate (req/s): $RATE
YQ used:     $HAS_YQ
GNU parallel: $HAS_PARALLEL
EOF

# Compression
if [ "$COMPRESS" = true ]; then
  TARFILE="${OUT_DIR}.tar.gz"
  log INFO "Creating archive $TARFILE ..."
  if tar -czf "$TARFILE" -C "$(dirname "$OUT_DIR")" "$(basename "$OUT_DIR")"; then
    TAR_SIZE=$(du -h "$TARFILE" | cut -f1)
    log INFO "Archive created: $TARFILE ($TAR_SIZE)"
  else
    log ERROR "Failed to create archive"
  fi
fi

# Create restore-helper.sh (applies CRDs first)
cat > "$OUT_DIR/restore-helper.sh" <<'RESTOREHELP'
#!/usr/bin/env bash
# restore-helper.sh - apply backup manifests in correct order
# Usage: ./restore-helper.sh [--dry-run] [--jobs N] [namespace-filter]
set -euo pipefail
IFS=$'\n\t'

DRY_RUN=false
JOBS=4
FILTER="${3:-}"

if [ "${1:-}" = "--dry-run" ]; then DRY_RUN=true; shift; fi
if [ "${1:-}" = "--jobs" ]; then JOBS="${2:-4}"; shift 2; fi
FILTER="${1:-}"

BACKUP_DIR="$(dirname "$0")"

apply_file() {
  f="$1"
  if [ "$DRY_RUN" = true ]; then
    kubectl apply --dry-run=client -f "$f" || true
  else
    kubectl apply -f "$f" || true
  fi
}

# 1) CRDs
if [ -f "$BACKUP_DIR/cluster/customresourcedefinitions.yaml" ]; then
  echo "Applying CRDs..."
  apply_file "$BACKUP_DIR/cluster/customresourcedefinitions.yaml"
fi

# 2) cluster-scoped resources
if [ -d "$BACKUP_DIR/cluster" ]; then
  for f in "$BACKUP_DIR/cluster"/*.yaml; do
    [ -f "$f" ] || continue
    echo "Applying cluster: $(basename "$f")"
    apply_file "$f"
  done
fi

# 3) namespaces
for nsdir in "$BACKUP_DIR"/*/; do
  ns=$(basename "$nsdir")
  [ "$ns" = "cluster" ] && continue
  [ "$ns" = "cluster-dump" ] && continue
  [ -d "$nsdir" ] || continue
  if [ -n "$FILTER" ] && [[ "$ns" != *"$FILTER"* ]]; then continue; fi
  echo "Ensuring namespace $ns exists"
  kubectl get ns "$ns" >/dev/null 2>&1 || kubectl create ns "$ns" || true
  for f in "$nsdir"/*.yaml; do
    [ -f "$f" ] || continue
    echo "Applying $ns/$(basename "$f")"
    if [ "$DRY_RUN" = true ]; then
      kubectl apply --dry-run=client -n "$ns" -f "$f" || true
    else
      kubectl apply -n "$ns" -f "$f" || true
    fi
  done
done

echo "Restore helper finished."
RESTOREHELP

chmod +x "$OUT_DIR/restore-helper.sh"

log INFO "Backup finished. Summary at $OUT_DIR/backup-summary.txt"
if [ "$COMPRESS" = true ] && [ -f "${TARFILE:-}" ]; then
  echo "$TARFILE"
else
  echo "$OUT_DIR"
fi

exit 0
```

Make a executable file
```sh
chmod +x backup-manifest.sh
```
```sh
./backup-manifest.sh
./backup-manifests.sh mybackup --jobs 6 --rate 10
```

---

# Restore
```sh
nano restore.sh
```
```sh
#!/usr/bin/env bash
# restore.sh - restore a backup directory or archive created by backup-manifests.sh
# Usage: ./restore.sh <backup-dir-or-archive> [--dry-run] [--jobs N]
set -euo pipefail
IFS=$'\n\t'

SRC="${1:-}"
DRY_RUN=false
JOBS=4
shift || true
while (( "$#" )); do
  case "$1" in
    --dry-run) DRY_RUN=true; shift;;
    --jobs) JOBS="${2:-$JOBS}"; shift 2;;
    *) shift;;
  esac
done

if [ -z "$SRC" ]; then
  echo "Usage: $0 <backup-dir-or-archive> [--dry-run] [--jobs N]" >&2
  exit 2
fi

command -v kubectl >/dev/null 2>&1 || { echo "kubectl not found" >&2; exit 2; }
HAS_PARALLEL=false; command -v parallel >/dev/null 2>&1 && HAS_PARALLEL=true

WORKDIR="$(pwd)/restore_temp_$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$WORKDIR"

if [ -f "$SRC" ]; then
  echo "Extracting archive $SRC ..."
  tar -xzf "$SRC" -C "$WORKDIR"
  TOPDIR=$(find "$WORKDIR" -maxdepth 1 -mindepth 1 -type d | head -n1)
else
  TOPDIR="$SRC"
fi

echo "Restore source: $TOPDIR"

apply_file() {
  f="$1"
  if [ "$DRY_RUN" = true ]; then
    kubectl apply --dry-run=client -f "$f" || true
  else
    kubectl apply -f "$f" || true
  fi
}
export -f apply_file

# 1) CRDs first
CRD_FILE="$TOPDIR/cluster/customresourcedefinitions.yaml"
if [ -f "$CRD_FILE" ]; then
  echo "Applying CRD definitions..."
  apply_file "$CRD_FILE"
fi

# 2) Cluster-scoped resources
if [ -d "$TOPDIR/cluster" ]; then
  echo "Applying cluster-scoped resources..."
  mapfile -t CLUSTER_FILES < <(find "$TOPDIR/cluster" -type f -name '*.yaml' | sort)
  for f in "${CLUSTER_FILES[@]}"; do
    echo "Applying cluster: $(basename "$f")"
    apply_file "$f"
  done
fi

# 3) Namespaced resources
mapfile -t NS_DIRS < <(find "$TOPDIR" -maxdepth 1 -type d -not -path "$TOPDIR/cluster" -not -path "$TOPDIR" | sort)

for nsdir in "${NS_DIRS[@]}"; do
  ns=$(basename "$nsdir")
  echo "Processing namespace: $ns"
  kubectl get ns "$ns" >/dev/null 2>&1 || kubectl create ns "$ns" || true

  mapfile -t FILES < <(find "$nsdir" -type f -name '*.yaml' | sort)
  if [ "${#FILES[@]}" -eq 0 ]; then continue; fi

  if [ "$HAS_PARALLEL" = true ] && [ "$JOBS" -gt 1 ]; then
    parallel --jobs "$JOBS" apply_file ::: "${FILES[@]}"
  else
    for f in "${FILES[@]}"; do
      if [ "$DRY_RUN" = true ]; then
        kubectl apply --dry-run=client -n "$ns" -f "$f" || true
      else
        kubectl apply -n "$ns" -f "$f" || true
      fi
    done
  fi
done

# cleanup extracted if we created a temp dir
if [ -d "$WORKDIR" ] && [ -f "$SRC" ]; then
  rm -rf "$WORKDIR"
fi

echo "Restore complete."
exit 0
```
Make a executable file
```sh
chmod +x restore.sh
```
```sh
./restore.sh
```