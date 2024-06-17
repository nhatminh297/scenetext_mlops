import numpy as np
from shapely.geometry import Polygon
from scipy.optimize import linear_sum_assignment

def iou(boxA, boxB):
    polyA = Polygon(boxA)
    polyB = Polygon(boxB)
    if not polyA.is_valid or not polyB.is_valid:
        return 0.0
    inter_area = polyA.intersection(polyB).area
    union_area = polyA.area + polyB.area - inter_area
    return inter_area / union_area

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def cer(s1, s2):
    return levenshtein_distance(s1, s2) / len(s2)

def wer(s1, s2):
    s1_words = s1.split()
    s2_words = s2.split()
    return levenshtein_distance(s1_words, s2_words) / len(s2_words)

def calculate_cost_matrix(predictions, ground_truths):
    cost_matrix = np.zeros((len(predictions), len(ground_truths)))
    for i, pred in enumerate(predictions):
        for j, gt in enumerate(ground_truths):
            iou_score = iou(pred[0], gt[0])
            text_distance = levenshtein_distance(pred[1], gt[1])
            cost_matrix[i, j] = 1 - iou_score + text_distance  # Có thể điều chỉnh trọng số của IoU và text distance
    return cost_matrix

def calculate_text_cost_matrix(predictions, ground_truths):
    cost_matrix = np.zeros((len(predictions), len(ground_truths)))
    for i, pred in enumerate(predictions):
        for j, gt in enumerate(ground_truths):
            text_distance = levenshtein_distance(pred[1], gt[1])
            cost_matrix[i, j] = text_distance
    return cost_matrix

def precision_recall_f1(predictions, ground_truths, iou_threshold=0.5):
    cost_matrix = calculate_cost_matrix(predictions, ground_truths)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    true_positives = 0
    false_positives = len(predictions)
    false_negatives = len(ground_truths)

    for i, j in zip(row_ind, col_ind):
        if iou(predictions[i][0], ground_truths[j][0]) >= iou_threshold:
            true_positives += 1
            false_positives -= 1
            false_negatives -= 1

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score

def precision_recall_f1_text(predictions, ground_truths, distance_threshold=0):
    cost_matrix = calculate_text_cost_matrix(predictions, ground_truths)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    true_positives = 0
    false_positives = len(predictions)
    false_negatives = len(ground_truths)

    for i, j in zip(row_ind, col_ind):
        if levenshtein_distance(predictions[i][1], ground_truths[j][1]) <= distance_threshold:
            true_positives += 1
            false_positives -= 1
            false_negatives -= 1

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score

def avg_metric(GTs, Preds):
    # Initialize cumulative metric sums
    avg_iou_precision = avg_iou_recall = avg_iou_f1 = 0
    avg_text_precision = avg_text_recall = avg_text_f1 = 0
    avg_cer = avg_wer = 0
    text_count = 0
    
    # Iterate over each pair of ground truths and predictions
    for gt, pred in zip(GTs, Preds):
        # Calculate the cost matrix and solve the assignment problem
        cost_matrix = calculate_cost_matrix(pred, gt)
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        # Iterate over matched pairs (pred, gt)
        for i, j in zip(row_ind, col_ind):
            pred_box, pred_text = pred[i]  # Access prediction pair correctly
            gt_box, gt_text = gt[j]
            text_count += 1
            avg_cer += cer(pred_text, gt_text)
            avg_wer += wer(pred_text, gt_text)
    
        # Calculate IOU precision, recall, and F1 for current pair
        iou_precision, iou_recall, iou_f1 = precision_recall_f1(pred, gt)
        avg_iou_precision += iou_precision
        avg_iou_recall += iou_recall
        avg_iou_f1 += iou_f1
        
        # Calculate text precision, recall, and F1 for current pair
        text_precision, text_recall, text_f1 = precision_recall_f1_text(pred, gt)
        avg_text_precision += text_precision
        avg_text_recall += text_recall
        avg_text_f1 += text_f1
    
    t = len(Preds)
    if text_count > 0:
        avg_cer /= text_count
        avg_wer /= text_count
    else:
        avg_cer = avg_wer = float('nan')  # Handle zero text count case
    
    return (avg_cer, avg_wer,
            avg_iou_precision / t if t > 0 else float('nan'),
            avg_iou_recall / t if t > 0 else float('nan'),
            avg_iou_f1 / t if t > 0 else float('nan'),
            avg_text_precision / t if t > 0 else float('nan'),
            avg_text_recall / t if t > 0 else float('nan'),
            avg_text_f1 / t if t > 0 else float('nan'))
