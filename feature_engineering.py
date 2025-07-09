import pandas as pd


def engineer_features(logon_file, file_file, email_file, psychometric_file):
    # Read uploaded files
    logon_df = pd.read_csv(logon_file)
    file_df = pd.read_csv(file_file)
    email_df = pd.read_csv(email_file)
    psychometric_df = pd.read_csv(psychometric_file)

    # ===================== LOGON FEATURES =====================
    logon_df['datetime'] = pd.to_datetime(logon_df['date'], errors='coerce')
    logon_df['hour'] = logon_df['datetime'].dt.hour
    logon_df['weekday'] = logon_df['datetime'].dt.weekday

    logons = logon_df[logon_df['activity'].str.lower() == 'logon']
    logoffs = logon_df[logon_df['activity'].str.lower() == 'logoff']

    total_logons = logons.groupby('user').size().reset_index(name='total_logons')
    logons['after_hours'] = logons['hour'].apply(lambda h: int(h < 8 or h > 18))
    after_hours_logons = logons.groupby('user')['after_hours'].sum().reset_index(name='after_hours_logons')
    
    logons['is_weekend'] = logons['weekday'].apply(lambda d: int(d >= 5))
    weekend_logons = logons.groupby('user')['is_weekend'].sum().reset_index(name='weekend_logons')    
    unique_machines = logons.groupby('user')['pc'].nunique().reset_index(name='unique_machines_used')
    avg_logon_hour = logons.groupby('user')['hour'].mean().reset_index(name='avg_logon_hour')
    logon_count = logons.groupby('user').size().reset_index(name='logon_count')
    logoff_count = logoffs.groupby('user').size().reset_index(name='logoff_count')
    log_ratio = pd.merge(logon_count, logoff_count, on='user', how='outer').fillna(0)
    log_ratio['logon_logoff_ratio'] = log_ratio['logon_count'] / (log_ratio['logoff_count'] + 1)
    logon_logoff_ratio = log_ratio[['user', 'logon_logoff_ratio']]

    features_logon = total_logons.merge(after_hours_logons, on='user', how='outer') \
        .merge(weekend_logons, on='user', how='outer') \
        .merge(unique_machines, on='user', how='outer') \
        .merge(avg_logon_hour, on='user', how='outer') \
        .merge(logon_logoff_ratio, on='user', how='outer')
    features_logon.fillna(0, inplace=True)

    # ===================== FILE FEATURES =====================
    file_df['datetime'] = pd.to_datetime(file_df['date'], errors='coerce')

    usb_file_writes = file_df[file_df['to_removable_media'] == True].groupby('user').size().reset_index(name='usb_file_writes')
    usb_file_reads = file_df[file_df['from_removable_media'] == True].groupby('user').size().reset_index(name='usb_file_reads')
    unique_files_accessed = file_df.groupby('user')['filename'].nunique().reset_index(name='unique_files_accessed')

    total_actions = file_df.groupby('user').size().reset_index(name='total_actions')
    write_actions = file_df[file_df['activity'].str.contains('Write', case=False, na=False)].groupby('user').size().reset_index(name='write_actions')
    file_write_ratio = pd.merge(total_actions, write_actions, on='user', how='left').fillna(0)
    file_write_ratio['file_write_ratio'] = file_write_ratio['write_actions'] / (file_write_ratio['total_actions'] + 1)
    file_write_ratio = file_write_ratio[['user', 'file_write_ratio']]

    keywords = ['secret', 'confidential', 'password', 'private', 'internal']
    file_df['is_sensitive'] = file_df['filename'].str.contains('|'.join(keywords), case=False, na=False).astype(int)
    sensitive_file_accesses = file_df.groupby('user')['is_sensitive'].sum().reset_index(name='sensitive_file_accesses')

    burst_scores = []
    for user, group in file_df.groupby('user'):
        group = group.sort_values('datetime')
        time_diffs = group['datetime'].diff().dt.total_seconds().fillna(99999)
        burst_count = (time_diffs <= 300).sum()
        burst_scores.append({'user': user, 'burst_file_activity_score': burst_count})
    burst_file_activity_score = pd.DataFrame(burst_scores)

    features_file = usb_file_writes.merge(usb_file_reads, on='user', how='outer') \
        .merge(unique_files_accessed, on='user', how='outer') \
        .merge(file_write_ratio, on='user', how='outer') \
        .merge(sensitive_file_accesses, on='user', how='outer') \
        .merge(burst_file_activity_score, on='user', how='outer')
    features_file.fillna(0, inplace=True)

    # ===================== EMAIL FEATURES =====================
    email_df['datetime'] = pd.to_datetime(email_df['date'], errors='coerce')
    email_df['hour'] = email_df['datetime'].dt.hour
    emails_sent = email_df[email_df['activity'].str.lower() == 'send'].groupby('user').size().reset_index(name='emails_sent')
    emails_with_attachments = email_df[email_df['attachments'].notnull()].groupby('user').size().reset_index(name='emails_with_attachments')

    after_hours = email_df[(email_df['activity'].str.lower() == 'send') & ((email_df['hour'] < 8) | (email_df['hour'] > 18))]
    after_hours_emails = after_hours.groupby('user').size().reset_index(name='after_hours_emails')

    avg_email_size = email_df[email_df['activity'].str.lower() == 'send'].groupby('user')['size'].mean().reset_index(name='avg_email_size')

    external_domain_emails = email_df[email_df['to'].str.contains('@', na=False)].groupby('user').size().reset_index(name='external_domain_emails')
    
    burst_scores = []
    for user, group in email_df.groupby('user'):
        group = group.sort_values('datetime')
        time_diffs = group['datetime'].diff().dt.total_seconds().fillna(99999)
        burst_count = (time_diffs <= 300).sum()
        burst_scores.append({'user': user, 'burst_email_activity_score': burst_count})
    burst_email_activity_score = pd.DataFrame(burst_scores)

    features_email = emails_sent.merge(after_hours_emails, on='user', how='outer') \
        .merge(emails_with_attachments, on='user', how='outer') \
        .merge(avg_email_size, on='user', how='outer') \
        .merge(external_domain_emails, on='user', how='outer')\
        .merge(burst_email_activity_score, on='user', how='outer')
    features_email.fillna(0, inplace=True)

    # ===================== PSYCHOMETRIC FEATURES =====================
    psychometric_df['personality_risk_index'] = (
    psychometric_df['O'] * 0.2 +
    (100 - psychometric_df['C']) * 0.25 +
    psychometric_df['N'] * 0.25 +
    psychometric_df['E'] * 0.15 +
    (100 - psychometric_df['A']) * 0.15)

    features_psycho = psychometric_df[['user', 'personality_risk_index']]

    # ===================== MERGE ALL FEATURES =====================
    merged_features = features_logon.merge(features_file, on='user', how='outer') \
        .merge(features_email, on='user', how='outer') \
        .merge(features_psycho, on='user', how='outer')

    merged_features.fillna(0, inplace=True)
    merged_features.set_index('user', inplace=True)

    return merged_features

