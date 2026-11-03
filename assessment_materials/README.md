# MSE806 Assessment 2 Group Materials

## 组员先看

这个目录包含本次小组作业的正式要求、Proposal、Report、PPT、Transcript、Turnitin 查重报告和最终检查清单。Turnitin 查重结果文件已经下载并放入本目录，最终打包提交时应一并保留。

三位成员分别录制自己的部分：

| 成员 | 学号 | 角色 | PPT 部分 | 建议时长 |
| --- | --- | --- | --- | --- |
| Xiaotong Sun | 270876224 | Data and Model Engineer | Slides 1–4 | 3–5 分钟 |
| Jingbiao Geng | 270686148 | API and Security Engineer | Slides 5–8 | 3–5 分钟 |
| Han Jia | 270902385 | Evaluation and Communication Lead | Slides 9–12 | 3–5 分钟 |

录制前先阅读自己的 transcript，不要只逐字朗读。需要能够解释自己负责的实现、结果和限制。三段视频合计不得超过 15 分钟。

## Assignment requirements

The official brief defines this assessment as a three-person ITS group project with two connected tasks:

- Task A: propose an ITS project, including its title, objectives, technological innovation and ethical considerations.
- Task B: implement the project and assess methodology, results, efficiency, security, limitations, contributions and lessons learned.
- The written report must contain 2,500 to 3,000 words and use APA-style references.
- The final submission must include the report, implementation files, demonstration files, slides and a recorded presentation.
- The combined presentation for Task A and Task B must not exceed 15 minutes.
- The official brief asks for a Turnitin originality result of 20 percent or lower and says that the downloaded Turnitin report should be included in the final submission. One group member can coordinate the similarity check, but the group should confirm the latest Blackboard instruction before uploading.
- The final Blackboard upload should be one ZIP file containing all required materials.

The exact calendar deadline and upload size limit should be checked on Blackboard because the supplied brief identifies Week 15 but does not give a final date and time.

## Files in this directory

| File | Purpose |
| --- | --- |
| `MSE806_Assessment2_Official_Brief.pdf` | Formal assessment instructions and marking rubric |
| `MSE806_Assessment2_Project_Proposal.docx` | Task A proposal |
| `MSE806_Assessment2_Project_Report.docx` | Task B report, including implementation, evaluation, security and contributions |
| `MSE806_Assessment2_Project_Report_Similarity.pdf` | Downloaded Turnitin similarity report for the project report; include it in the final submission package |
| `MSE806_Assessment2_Three_Person_Presentation.pptx` | Twelve-slide group presentation |
| `MSE806_Assessment2_Presentation_Transcript.docx` | Speaker script divided into three presenter parts |
| `FINAL_SUBMISSION_CHECKLIST.md` | Final Turnitin, recording and ZIP checks |

## Presenter instructions

### Part 1 Xiaotong Sun

Slides 1–4 cover:

- project title and group structure;
- traffic forecasting problem and objectives;
- open-source starting point and assessed contribution;
- synthetic data, chronological split and model methodology.

End by handing over to Jingbiao Geng.

### Part 2 Jingbiao Geng

Slides 5–8 cover:

- system architecture;
- API authentication, input validation, CORS, request limits and logging;
- five automated security and functionality tests;
- working dashboard demonstration and production security limitations.

End by handing over to Han Jia.

### Part 3 Han Jia

Slides 9–12 cover:

- evaluation design and persistence baseline;
- MAE, RMSE, R squared and the 40.39 percent MAE improvement;
- current limitations and future development steps;
- conclusion and the three-person contribution record.

End the complete presentation after slide 12.

## Recording workflow

1. Download or clone the repository and open the PowerPoint in presentation mode.
2. Use a quiet room and record in 16:9 landscape format at 1080p when available.
3. Show only the slides assigned to your part. Do not display personal notifications or unrelated browser tabs.
4. Use the transcript as a guide. Speak naturally and explain the evidence rather than reading every sentence exactly.
5. Keep technical values consistent with the report: 17,280 records, 3,456 validation records, MAE 2.6083 km/h, RMSE 3.2803 km/h, R squared 0.8247, 40.39 percent MAE improvement and five passing tests.
6. Name separate recordings `Part1_Xiaotong_Sun.mp4`, `Part2_Jingbiao_Geng.mp4` and `Part3_Han_Jia.mp4`.
7. Combine the recordings in slide order, check audio levels and confirm the final video is below 15 minutes.
8. Do not commit the final MP4 to GitHub if it is large. Share it through the agreed drive or upload method and place it in the final Blackboard ZIP.

## Running the demonstration

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_data.py
python train_model.py
python evaluate_models.py
pytest -q
```

Start the API and dashboard in separate terminals:

```bash
TRAFFIC_API_KEY=mse806-demo-key uvicorn run_dashboard:app --host 127.0.0.1 --port 8000
python -m http.server 8001
```

Open `http://127.0.0.1:8001/dashboard.html` and use the local demonstration key shown above.

Expected stable results:

- MAE: 2.6083 km/h
- RMSE: 3.2803 km/h
- R squared: 0.8247
- MAE improvement over persistence: 40.39 percent
- Automated tests: 5 passed

## Final submission checklist

Before Blackboard upload, confirm the final ZIP contains:

- proposal;
- final report;
- source code, requirements, model, generated results and demonstration files;
- PowerPoint slides;
- combined presentation MP4;
- presentation transcript;
- downloaded Turnitin similarity report (`MSE806_Assessment2_Project_Report_Similarity.pdf`), which is already included in this directory.

Every member should confirm that their name, student ID and contribution are correct before the group submits.
