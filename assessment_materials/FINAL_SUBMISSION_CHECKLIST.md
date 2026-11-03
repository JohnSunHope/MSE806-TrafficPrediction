# MSE806 Assessment 2 Final Submission Checklist

## Confirm group details

- Confirm the names and student IDs: Xiaotong Sun 270876224, Jingbiao Geng 270686148 and Han Jia 270902385.
- Confirm that each member agrees with the contribution record and can explain their own implementation work.

## Record the presentation

- Use the supplied PowerPoint and transcript.
- Xiaotong Sun presents slides 1 to 4 as the Data and Model Engineer.
- Jingbiao Geng presents slides 5 to 8 as the API and Security Engineer.
- Han Jia presents slides 9 to 12 as the Evaluation and Communication Lead.
- Keep each part between 3 and 5 minutes and the combined recording below 15 minutes.
- Add the finished MP4 recording to the submission folder before creating the Blackboard ZIP.

## Run the final demonstration check

```bash
cd Project_Code
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_data.py
python train_model.py
python evaluate_models.py
python -m pytest -q
```

The expected stable model results are MAE 2.6083 km/h, RMSE 3.2803 km/h and R squared 0.8247. Inference timing varies slightly between runs. The tests should report five passed.

## Turnitin and Blackboard

- Submit the report to the MSE806 Assessment 2 Turnitin location using the member nominated by the group.
- Confirm the current classroom and Blackboard instructions for whether the downloaded Turnitin report must be included. The formal V2 PDF says to include it, while the latest classroom checklist leaves the attachment detail to be confirmed.
- Check the final originality report and revise genuine citation or quotation problems rather than changing technical terms only to reduce a number.
- Put the proposal, report, code, model, results, slides, transcript, recorded presentation and any required Turnitin report into one ZIP.
- Open the final ZIP once and confirm every file can be read before uploading to Blackboard.
