from sys import argv
from time import sleep
import pandas as pd
from ipaddress import ip_address, ip_network
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt
from datetime import timedelta as td
import numpy as np
import ipinfo
import json
import socket
from subprocess import Popen, PIPE, STDOUT, check_output
import os


zoom_nets = ['3.7.35.0/25','3.21.137.128/25','3.22.11.0/24','3.23.93.0/24','3.25.41.128/25',
             '3.25.42.0/25','3.25.49.0/24', '3.80.20.128/25','3.96.19.0/24','3.101.32.128/25','3.101.52.0/25','3.104.34.128/25','3.120.121.0/25','3.127.194.128/25','3.208.72.0/25','3.211.241.0/25','3.235.69.0/25','3.235.71.128/25','3.235.72.128/25','3.235.73.0/25','3.235.82.0/23','3.235.96.0/23','4.34.125.128/25','4.35.64.128/25','8.5.128.0/23','13.52.6.128/25','13.52.146.0/25','15.220.80.0/24','15.220.81.0/25','18.157.88.0/24','18.205.93.128/25','18.254.23.128/25','18.254.61.0/25','20.203.158.80/28','20.203.190.192/26','50.239.202.0/23','50.239.204.0/24','52.61.100.128/25','52.84.151.0/24','52.202.62.192/26','52.215.168.0/25','64.125.62.0/24','64.211.144.0/24','64.224.32.0/19','65.39.152.0/24','69.174.57.0/24','69.174.108.0/22','99.79.20.0/25','101.36.167.0/24','101.36.170.0/23','103.122.166.0/23','111.33.115.0/25','111.33.181.0/25','115.110.154.192/26','115.114.56.192/26','115.114.115.0/26','115.114.131.0/26','120.29.148.0/24','129.151.1.128/27','129.151.1.192/27','129.151.2.0/27','129.151.3.160/27','129.151.7.96/27','129.151.11.64/27','129.151.11.128/27','129.151.12.0/27','129.151.13.64/27','129.151.15.224/27','129.151.16.0/27','129.151.31.224/27','129.151.40.0/25','129.151.40.160/27','129.151.40.192/27','129.151.41.0/25','129.151.41.192/26','129.151.42.0/27','129.151.42.64/27','129.151.42.128/26','129.151.42.224/27','129.151.43.0/27','129.151.43.64/26','129.151.48.0/27','129.151.48.160/27','129.151.49.0/26','129.151.49.96/27','129.151.49.128/27','129.151.49.192/26','129.151.50.0/27','129.151.50.64/27','129.151.52.128/26','129.151.53.32/27','129.151.53.224/27','129.151.55.32/27','129.151.56.32/27','129.151.57.32/27','129.151.60.192/27','129.159.2.32/27','129.159.2.192/27','129.159.3.0/24','129.159.4.0/23','129.159.6.0/27','129.159.6.96/27','129.159.6.128/26','129.159.6.192/27','129.159.160.0/26','129.159.160.64/27','129.159.163.0/26','129.159.163.160/27','129.159.208.0/21','129.159.216.0/26','129.159.216.64/27','129.159.216.128/26','130.61.164.0/22','132.226.176.0/25','132.226.176.128/26','132.226.177.96/27','132.226.177.128/25','132.226.178.0/27','132.226.178.128/27','132.226.178.224/27','132.226.179.0/27','132.226.179.64/27','132.226.180.128/27','132.226.183.160/27','132.226.185.192/27','134.224.0.0/16','140.238.128.0/24','140.238.232.0/22','144.195.0.0/16','147.124.96.0/19','149.137.0.0/17','150.230.224.0/25','150.230.224.128/26','150.230.224.224/27','152.67.20.0/24','152.67.118.0/24','152.67.168.0/22','152.67.180.0/24','152.67.184.32/27','152.67.240.0/21','152.70.0.0/25','152.70.0.128/26','152.70.0.224/27','152.70.1.0/25','152.70.1.128/26','152.70.1.192/27','152.70.2.0/26','152.70.7.192/27','152.70.10.32/27','152.70.224.32/27','152.70.224.64/26','152.70.224.160/27','152.70.224.192/27','152.70.225.0/25','152.70.225.160/27','152.70.225.192/27','152.70.226.0/27','152.70.227.96/27','152.70.227.192/27','152.70.228.0/27','152.70.228.64/27','152.70.228.128/27','156.45.0.0/17','158.101.64.0/24','158.101.184.0/23','158.101.186.0/25','158.101.186.128/27','158.101.186.192/26','158.101.187.0/25','158.101.187.160/27','158.101.187.192/26','159.124.0.0/16','160.1.56.128/25','161.199.136.0/22','162.12.232.0/22','162.255.36.0/22','165.254.88.0/23','166.108.64.0/18','168.138.16.0/22','168.138.48.0/24','168.138.56.0/21','168.138.72.0/24','168.138.74.0/25','168.138.80.0/25','168.138.80.128/26','168.138.80.224/27','168.138.81.0/24','168.138.82.0/23','168.138.84.0/25','168.138.84.128/27','168.138.84.192/26','168.138.85.0/24','168.138.86.0/23','168.138.96.0/22','168.138.116.0/27','168.138.116.64/27','168.138.116.128/27','168.138.116.224/27','168.138.117.0/27','168.138.117.96/27','168.138.117.128/27','168.138.118.0/27','168.138.118.160/27','168.138.118.224/27','168.138.119.0/27','168.138.119.128/27','168.138.244.0/24','170.114.0.0/16','173.231.80.0/20','192.204.12.0/22','193.122.16.0/25','193.122.16.192/27','193.122.17.0/26','193.122.17.64/27','193.122.17.224/27','193.122.18.32/27','193.122.18.64/26','193.122.18.160/27','193.122.18.192/27','193.122.19.0/27','193.122.19.160/27','193.122.19.192/27','193.122.20.224/27','193.122.21.96/27','193.122.32.0/21','193.122.40.0/22','193.122.44.0/24','193.122.45.32/27','193.122.45.64/26','193.122.45.128/25','193.122.46.0/23','193.122.208.96/27','193.122.216.32/27','193.122.222.0/27','193.122.223.128/27','193.122.226.160/27','193.122.231.192/27','193.122.232.160/27','193.122.237.64/27','193.122.244.160/27','193.122.244.224/27','193.122.245.0/27','193.122.247.96/27','193.122.252.192/27','193.123.0.0/19','193.123.40.0/21','193.123.128.0/19','193.123.168.0/21','193.123.192.224/27','193.123.193.0/27','193.123.193.96/27','193.123.194.96/27','193.123.194.128/27','193.123.194.224/27','193.123.195.0/27','193.123.196.0/27','193.123.196.192/27','193.123.197.0/27','193.123.197.64/27','193.123.198.64/27','193.123.198.160/27','193.123.199.64/27','193.123.200.128/27','193.123.201.32/27','193.123.201.224/27','193.123.202.64/27','193.123.202.128/26','193.123.203.0/27','193.123.203.160/27','193.123.203.192/27','193.123.204.0/27','193.123.204.64/27','193.123.205.64/26','193.123.205.128/27','193.123.206.32/27','193.123.206.128/27','193.123.207.32/27','193.123.208.160/27','193.123.209.0/27','193.123.209.96/27','193.123.210.64/27','193.123.211.224/27','193.123.212.128/27','193.123.215.192/26','193.123.216.64/27','193.123.216.128/27','193.123.217.160/27','193.123.219.64/27','193.123.220.224/27','193.123.222.64/27','193.123.222.224/27','198.251.128.0/17','202.177.207.128/27','204.80.104.0/21','204.141.28.0/22','206.247.0.0/16','207.226.132.0/24','209.9.211.0/24','209.9.215.0/24','213.19.144.0/24','213.19.153.0/24','213.244.140.0/24','221.122.63.0/24','221.122.64.0/24','221.122.88.64/27','221.122.88.128/25','221.122.89.128/25','221.123.139.192/27']
zoom_ips = {}
non_zoom_ips = {}
metric_columns = ['pkts', 'frames', 'bytes']
type_color = {'a':'red', 'v':'green', 's':'blue'}
direction_color = {'from_zoom':'red', 'to_zoom':'green'}
zoom_types = {16 :'v', 15:'a', 13:'s', 34:'rtcp', 33:'rtcp'}

def which_is_zoom(ip_src):
  if ip_src in zoom_ips.keys():
    zoom_ips[ip_src]['count'] += 1
    return 'from_zoom'
  elif ip_src in non_zoom_ips.keys():
    non_zoom_ips[ip_src]['count'] += 1
    return 'to_zoom'
  else:
    for net in zoom_nets:
      if ip_address(ip_src) in ip_network(net):
        zoom_ips[ip_src] = {'count': 1}
        return 'from_zoom'
  non_zoom_ips[ip_src] = {'count': 1}
  return 'to_zoom'

def traceroute(ip):
  route = []
  traceroute = Popen(["traceroute", '-m', '30', '-w', '1', ip],stdout=PIPE, stderr=STDOUT)
  for line in iter(traceroute.stdout.readline,""):
    if line != b'':
      route.append(line.decode('ascii'))
    else:
      break
  return route

def ping(ip):
  result = []
  ping = Popen(["ping", '-c', '10', ip],stdout=PIPE, stderr=STDOUT)
  for line in iter(ping.stdout.readline,""):
    if line != b'':
      result.append(line.decode('ascii'))
    else:
      break
  return result

def server_location():
  access_token = '6ea74afd76ea25'
  handler = ipinfo.getHandler(access_token)
  for ip in zoom_ips:
    try:
      hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
      hostname = None
    details = handler.getDetails(ip)
    zoom_ips[ip]['region'] = details.region
    zoom_ips[ip]['country'] = details.country_name
    zoom_ips[ip]['hostname'] = hostname
    zoom_ips[ip]['traceroute'] = traceroute(ip)
    zoom_ips[ip]['ping'] = ping(ip)
  f = open("server_locations.txt", "w")
  f.write(json.dumps(dict(sorted(zoom_ips.items(), key = lambda x: x[1]['count'], reverse=True)), sort_keys=False, indent=2))
  f.close()

def connections(meetings):
  stalls = {}
  meetings['start_dt'] = meetings.apply(lambda row: dt.fromtimestamp(row.start_ts_s), axis = 1)
  meetings['end_dt'] = meetings.apply(lambda row: dt.fromtimestamp(row.end_ts_s), axis = 1)
  meetings['zoom_ip'] = meetings.apply(lambda row: which_is_zoom(row.ip_src), axis = 1)
  for meeting_id, meeting_group in meetings.groupby('meeting_id'):
    if meeting_id != -1:
      try:
        os.mkdir('./meeting_stats/Meeting_' + str(meeting_id) + '/')
      except FileExistsError:
        pass
    stall = False
    prev_end_dt = meeting_group['end_dt'].min()
    fig, ax = plt.subplots()
    colormap = plt.cm.nipy_spectral
    colors = colormap(np.linspace(0, 1, len(meeting_group['stream_id'].unique())))
    ax.set_prop_cycle('color', colors)
    y = 1
    for stream_id, stream_group in meeting_group.groupby('stream_id'):
      stream_group = stream_group.sort_values(['start_dt', 'end_dt'])
      xvals = [stream_group['start_dt'], stream_group['end_dt']]
      yvals = [y, y]

      #tracking connections
      if stall == False and stream_group['start_dt'].values[0] > prev_end_dt:
        stalls[str(meeting_id)] = {'start': str(pd.to_datetime(prev_end_dt)),
                              'end': str(pd.to_datetime(stream_group['start_dt'].values[0])),
                              'delay': str((stream_group['start_dt'].values[0] - prev_end_dt) / np.timedelta64(1, 's'))}
        stall = True
        plt.axvline(x = prev_end_dt, color = 'red', linestyle='--', label = 'stall start')
        plt.axvline(x = stream_group['start_dt'].values[0], color = 'green', linestyle='--', label = 'stall end')
      elif stream_group['end_dt'].values[0] > prev_end_dt:
        prev_end_dt = stream_group['end_dt'].values[0]


      if stream_group['zoom_ip'].values[0] == 'from_zoom':
        label = stream_group['ip_src'].values[0]
      else:
        label = stream_group['ip_dst'].values[0]
      plt.plot(xvals, yvals, label = str('type: ' + zoom_types[stream_group['zoom_type'].values[0]] + ', ip :' + label))
      y += 1
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize='6')
    plt.savefig('./meeting_stats/Meeting_' + str(meeting_id) + '/connections.png')
    plt.close()
  return stalls

def jitter(group, stalls, id, title):
  fig, ax = plt.subplots()
  stat_graph = group.sort_values(['t_dt']).groupby('t_dt')['mean_jitter'].mean()
  stat_graph.plot(title= 'mean jitter by type', ylabel= 'mean jitter', xlabel= 'time (s)', ax=ax)
  if id in stalls:
    plt.axvline(x = stalls[id]['start'], color = 'red', linestyle='--', label = 'stall start')
    plt.axvline(x = stalls[id]['end'], color = 'green', linestyle='--', label = 'stall end')
    plt.axvline(x =(pd.to_datetime(stalls[id]['start']) - td(seconds=15)), color='black', linestyle='--')
    stalls[id]['mean jitter'] = {'pre stall' : round(stats[(stats['t_dt'] >= (pd.to_datetime(stalls[id]['start']) - td(seconds=15))) & (stats['t_dt'] <= pd.to_datetime(stalls[id]['start']))].groupby('t_dt')['mean_jitter'].sum().mean(numeric_only=True), 3),
                               'total' : round(stats.groupby('t_dt')['mean_jitter'].sum().mean(numeric_only=True), 3)}
  ax.legend(loc='upper right')
  plt.savefig(title + 'type_mean_jitter.png')
  plt.close()

  return stalls

def loss(stats, stalls, id, title):
  fig, ax = plt.subplots()
  stat_graph = stats.sort_values(['t_dt']).groupby('t_dt')['lost'].sum()
  stat_graph.plot(title= 'total loss', ylabel= 'lost packets', xlabel= 'time (s)', ax=ax)
  if id in stalls:
    plt.axvline(x = stalls[id]['start'], color = 'red', linestyle='--', label = 'stall start')
    plt.axvline(x = stalls[id]['end'], color = 'green', linestyle='--', label = 'stall end')
    plt.axvline(x =(pd.to_datetime(stalls[id]['start']) - td(seconds=60)), color='black', linestyle='--')
  plt.savefig(title + 'total_loss.png')
  plt.close()
  return stalls

def meeting_id(ip_src, ip_dst, rtp_ssrc, meetings):
  meeting_ids = meetings.loc[(meetings['ip_src'] == ip_src) & (meetings['ip_dst'] == ip_dst) & (meetings['ssrc'] == rtp_ssrc)]['meeting_id']
  try:
    meeting_id = meeting_ids.iloc[0]
  except IndexError:
    meeting_id = -1
  return int(meeting_id)

def number_meetings(stats):
  fig, ax = plt.subplots()  
  stat_graph = stats.sort_values(['t_dt']).groupby('t_dt')['meeting_id'].nunique()
  stat_graph.plot(title= 'Number of Meetings', ylabel= 'Number', xlabel= 'time (s)', 
                subplots=True, ax=ax)
  #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  plt.savefig('./meeting_stats/Number_of_Meeting.png')
  plt.close()
 
def direction_stats(stats, metric, id, title=''):
  fig, ax = plt.subplots()
  for name, group in stats.groupby('zoom_ip'):
    type_stats(group, metric, id, title='./meeting_stats/Meeting_' + str(id) + '/' + str(name) + '_')
    stat_graph = group.sort_values(['t_dt']).groupby('t_dt')[metric].sum()
    stat_graph.plot(title= metric + ' rate', label=name, ylabel= metric + ' per second', xlabel= 'time (s)', 
                subplots=True, legend=True, color=direction_color[name], ax=ax)
  #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  ax.legend(loc='upper right')
  plt.savefig(title + 'direction_' + metric + '_rate.png')
  plt.close()

def meeting_stats(stats, metric, stalls):
  for name, group in stats.groupby('meeting_id'):
    if name != -1:
      fig, ax = plt.subplots()
      #type_stats(group, metric, str(name), title='./meeting_stats/Meeting_' + str(name) + '/')
      #direction_stats(group, metric, str(name), title='./meeting_stats/Meeting_' + str(name) + '/')
      #stalls = jitter(group, stalls, str(name), title='./meeting_stats/Meeting_' + str(name) + '/')
      stalls = loss(group, stalls, str(name), title='./meeting_stats/Meeting_' + str(name) + '/')
      stat_graph = group.sort_values(['t_dt']).groupby('t_dt')[metric].sum()
      stat_graph.plot(title= 'Meeting ' + str(name) + ' total ' + metric + ' rate', ylabel= metric + ' per second', xlabel= 'time (s)', 
                    subplots=True, ax=ax)
      #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      if str(name) in stalls:
        plt.axvline(x = stalls[str(name)]['start'], color = 'red', linestyle='--', label = 'stall start')
        plt.axvline(x = stalls[str(name)]['end'], color = 'green', linestyle='--', label = 'stall end')
        plt.axvline(x =(pd.to_datetime(stalls[str(name)]['start']) - td(seconds=15)), color='black', linestyle='--')
      plt.savefig('./meeting_stats/Meeting_' + str(name) + '/total_' + metric + '_rate.png')
      plt.close()
  return stalls

def type_stats(stats, metric, id=None, title=''):
  fig, ax = plt.subplots()
  for name, group in stats.groupby('media_type'):
    stat_graph = group.sort_values(['t_dt']).groupby('t_dt')[metric].sum()
    stat_graph.plot(title= metric + ' rate', label=name, ylabel= metric + ' per second', xlabel= 'time (s)', 
                subplots=True, legend=True, color=type_color[name], ax=ax)
  #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  ax.legend(loc='upper right')
  plt.savefig(title + 'type_' + metric + '_rate.png')
  plt.close()

def overall_stats(stats, metric):
  fig, ax0 = plt.subplots()
  stat_graph = stats.sort_values(['t_dt']).groupby('t_dt')[metric].sum()
  stat_graph.plot(title= 'total ' + metric + ' rate', ylabel= metric + ' per second', xlabel= 'time (s)', 
                subplots=True, ax=ax0)
  ax1 = ax0.twinx() 
  stat_graph = stats.sort_values(['t_dt']).groupby('t_dt')['meeting_id'].nunique()
  stat_graph.plot(label='Number of Meetings', ylabel = 'number of meetings', subplots=True, legend=True, linestyle='dotted', color='orange', ax=ax1)
  #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  plt.savefig('./total_' + metric + '_rate.png')
  plt.close()

def handle_stats(stats, meetings):
  stats['zoom_ip'] = stats.apply(lambda row: which_is_zoom(row.ip_src), axis = 1)
  stats['t_dt'] = stats.apply(lambda row: dt.fromtimestamp(row.ts_s), axis = 1)
  stats['meeting_id'] = stats.apply(lambda row: meeting_id(row.ip_src, row.ip_dst, row.rtp_ssrc, meetings), axis = 1)
  stalls = connections(meetings)
  for metric in metric_columns:
    #overall_stats(stats, metric)
    #type_stats(stats, metric)
    stalls = meeting_stats(stats, metric, stalls)
  #server_location()
  #number_meetings(stats)

  try:
    os.mkdir('./stalls')
  except FileExistsError:
    pass
  f = open("./stalls/stalls.txt", "w")
  f.write(json.dumps(stalls, indent=2))
  f.close()


def handle_meetings(meetings):
  meetings_stats = {}
  meetings_stats['totals'] = {'pkts':int(meetings['pkts'].sum()),
                              'bytes':int(meetings['bytes'].sum()), 
                              'types':{'a':{'pkts':0,
                                            'bytes':0, 
                                            'types':{'112':{'pkts':int(meetings['audio_112_pkts'].sum())}, 
                                                      '99':{'pkts':int(meetings['audio_99_pkts'].sum())}, 
                                                      '113':{'pkts':int(meetings['audio_113_pkts'].sum())}}}, 
                                       'v':{'pkts':0, 'bytes':0}, 
                                       's':{'pkts':0, 'bytes':0}}}
  for name, group in meetings.groupby('meeting_id'):
    meetings_stats[name] = {'types':{}, 'totals':{}}
    meeting_pkts = group['pkts'].sum()
    meetings_stats[name]['totals']['pkts'] = int(meeting_pkts)
    meeting_bytes = group['bytes'].sum()
    meetings_stats[name]['totals']['bytes'] = int(meeting_bytes)
    meeting_type_pkts = group.groupby('zoom_type')['pkts'].sum()
    meeting_type_bytes = group.groupby('zoom_type')['bytes'].sum()
    for type in meeting_type_pkts.index:
      meetings_stats[name]['types'][zoom_types[type]] = {}
      meetings_stats[name]['types'][zoom_types[type]]['pkts'] = int(meeting_type_pkts[type])
      meetings_stats['totals']['types'][zoom_types[type]]['pkts'] += int(meeting_type_pkts[type])
      meetings_stats[name]['types'][zoom_types[type]]['bytes'] = int(meeting_type_bytes[type])
      meetings_stats['totals']['types'][zoom_types[type]]['bytes'] += int(meeting_type_bytes[type])
      meetings_stats[name]['types'][zoom_types[type]]['portion of total packets'] = round(float(int(meeting_type_pkts[type]) / int(meeting_pkts)), 3)
      meetings_stats[name]['types'][zoom_types[type]]['portion of total bytes'] = round(float(int(meeting_type_bytes[type]) / int(meeting_bytes)), 3)
      if type == 15:
        meetings_stats[name]['types'][zoom_types[type]]['types'] = {'112':{'pkts':int(group['audio_112_pkts'].sum()),
                                                                           'portion of audio packets':round(float(int(group['audio_112_pkts'].sum())/int(meetings_stats[name]['types'][zoom_types[type]]['pkts'])), 3)}, 
                                                                    '99':{'pkts':int(group['audio_99_pkts'].sum()),
                                                                           'portion of audio packets':round(float(int(group['audio_99_pkts'].sum())/int(meetings_stats[name]['types'][zoom_types[type]]['pkts'])), 3)}, 
                                                                    '113':{'pkts':int(group['audio_113_pkts'].sum()),
                                                                           'portion of audio packets':round(float(int(group['audio_113_pkts'].sum())/int(meetings_stats[name]['types'][zoom_types[type]]['pkts'])), 3)}}
  
  for key in meetings_stats['totals']['types']['a']['types']:
    meetings_stats['totals']['types']['a']['types'][key]['portion of audio packets'] = round(float(int(meetings_stats['totals']['types']['a']['types'][key]['pkts'])/int(meetings_stats['totals']['types']['a']['pkts'])), 3)

  for key in meetings_stats['totals']['types'].keys():
    meetings_stats['totals']['types'][key]['portion of total packets'] = round(float(int(meetings_stats['totals']['types'][key]['pkts']) / int(meetings_stats['totals']['pkts'])), 3)
    meetings_stats['totals']['types'][key]['portion of total bytes'] = round(float(int(meetings_stats['totals']['types'][key]['bytes']) / int(meetings_stats['totals']['bytes'])), 3)
  f = open("./meeting_stats/meetings_stats.txt", "w")
  f.write(json.dumps(meetings_stats, indent=2))
  f.close()

if __name__ == "__main__":
  try:
    os.mkdir('./meeting_stats')
  except FileExistsError:
    pass
  stats = pd.read_csv('./data/stats_anon.csv')
  meetings = pd.read_csv('./data/meetings_anon.csv')
  handle_stats(stats, meetings)
  #handle_meetings(meetings)
