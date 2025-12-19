from flask import Flask, request, render_template_string, send_from_directory
from ultralytics import YOLO
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Charger le modèle YOLOv8 classification
MODEL_PATH = "./best.pt"
model = YOLO(MODEL_PATH)

CONFIDENCE_THRESHOLD = 0.9998  # seuil pour dire "rien des deux"

@app.route("/", methods=["GET", "POST"])
def upload_and_predict():
    message = ""
    filename = ""
    predicted_class = ""
    confidence = 0.0

    if request.method == "POST":
        if "image" not in request.files:
            message = "Aucun fichier sélectionné"
        else:
            file = request.files["image"]
            if file.filename == "":
                message = "Aucun fichier sélectionné"
            else:
                # Sauvegarder le fichier
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                filename = file.filename
                message = f"Image téléchargée avec succès : {file.filename}"

                # Prédiction
                results = model(filepath)
                result = results[0]
                top1_index = result.probs.top1
                top1_conf = float(result.probs.top1conf)

                # Vérifier le seuil de confiance
                if top1_conf >= CONFIDENCE_THRESHOLD:
                    predicted_class = result.names[top1_index]
                    confidence = top1_conf
                else:
                    predicted_class = "Rien des deux"
                    confidence = top1_conf  # facultatif, montre la probabilité max quand même

    return render_template_string('''
        <!doctype html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Upload & Prédiction</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <div class="card shadow-sm">
                            <div class="card-body text-center">
                                <h3 class="card-title mb-4">Envoyer une image</h3>

                                {% if message %}
                                    <div class="alert alert-info">{{ message }}</div>
                                {% endif %}

                                <form method="POST" enctype="multipart/form-data">
                                    <div class="mb-3">
                                        <input class="form-control" type="file" name="image" accept="image/*" required>
                                    </div>
                                    <div class="d-grid">
                                        <button class="btn btn-primary" type="submit">Envoyer & Prédire</button>
                                    </div>
                                </form>

                                {% if filename %}
                                    <div class="mt-4">
                                        <h5>Classe prédite : <strong>{{ predicted_class }}</strong></h5>
                                        <h6>Confiance : {{ confidence*100 | round(2) }}%</h6>
                                        <img src="{{ url_for('uploaded_file', filename=filename) }}" class="img-fluid mt-3 shadow-sm" alt="Image">
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''', message=message, filename=filename, predicted_class=predicted_class, confidence=confidence)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
