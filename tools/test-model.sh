REPO_DIR="data/spacy-models"

[[ -d "$REPO_DIR" ]] || git clone https://github.com/explosion/spacy-models.git "$REPO_DIR"
cd "$REPO_DIR"

pip install -r tests/requirements.txt
py.test tests --model ../nb-lg --lang nb --has-parser --has-tagger --has-ner


