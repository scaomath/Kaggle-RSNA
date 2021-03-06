import os
import pandas as pd
import numpy as np
from dataset import LABEL_COLS


if __name__ == '__main__':
    target_cols = LABEL_COLS
    test_csv = "./csv/patient2_kfold/test.csv"
    pred_paths = [
        '/logs/prediction/densenet169-mw-512-resume-0/test_0_ckp_tta.npy',
        '/logs/prediction/densenet169-mw-512-resume-1/test_1_ckp_tta.npy',
        '/logs/prediction/densenet169-mw-512-resume-2/test_2_ckp_tta.npy',
        "/logs/prediction/densenet169-mw-512-resume-3/test_3_ckp_tta.npy",
        "/logs/prediction/densenet169-mw-512-resume-4/test_4_ckp_tta.npy"
        # '/logs/predictions/se_resnext50_32x4d-mw-512-recheck-0/test_0.npy',
    ]

    test_preds = 0
    for pred in pred_paths:
        test_preds += np.load(pred)

    test_preds = test_preds / len(pred_paths)

    test_df = pd.read_csv(test_csv)
    test_df["sop_instance_uid"] = "ID_" + test_df["sop_instance_uid"]
    test_ids = test_df['sop_instance_uid'].values

    ids = []
    labels = []
    for i, id in enumerate(test_ids):
        pred = test_preds[i]
        for j, target in enumerate(target_cols):
            id_target = id + "_" + target
            ids.append(id_target)
            labels.append(pred[j])
        # if not with_any:
        #     id_target = id + "_" + "any"
        #     ids.append(id_target)
        #     labels.append(pred.max())

    submission_df = pd.DataFrame({
        'ID': ids,
        'Label': labels
    })

    os.makedirs(f"/logs/prediction/ensemble/", exist_ok=True)

    submission_df.to_csv(f"/logs/prediction/ensemble/densenet169-mww-512-5folds_tta.csv", index=False)
