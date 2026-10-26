"""Revision figures from independently recomputed values; historical PNGs are retained."""
from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data/results'
s=json.loads((D/'summary.json').read_text());pairs=list(csv.DictReader((D/'pairs_recomputed.csv').open()))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
fig,ax=plt.subplots(figsize=(7.15,4.1));fig.subplots_adjust(left=.13,right=.98,top=.86,bottom=.32)
values=[s['frames'][x] for x in ['A','B0','Bomega']];cols=['#718193','#28798E','#B56537']
ax.bar(range(3),values,color=cols,width=.60,zorder=3)
ax.set_ylim(0,347000);ax.yaxis.set_major_formatter(FuncFormatter(lambda v,pos:f'{v/1000:g}'))
ax.set_ylabel('Saved frames (thousands)');ax.set_xticks(range(3),['A\nSaved ensemble',r'$B_0$'+'\nGeometry pass',r'$B_\omega$'+'\nGeometry + omega pass']);ax.grid(axis='y',alpha=.18,zorder=0)
for i,v in enumerate(values):ax.text(i,v+6500,f'{v:,}',ha='center',va='bottom',weight='bold',fontsize=12)
fig.text(.13,.95,'154 systems | pooled retained frame counts',weight='bold',fontsize=11)
fig.text(.96,.91,r'$A\supseteq B_0\supseteq B_\omega$',ha='right',fontsize=13)
fig.text(.13,.14,r'$A\rightarrow B_0$: 4,612 / 302,800 excluded (1.523% of A)',fontsize=10)
fig.text(.13,.085,r'$B_0\rightarrow B_\omega$: 25,807 / 298,188 excluded (8.655% of $B_0$)',fontsize=10)
for ext in ['png','pdf','svg']:fig.savefig(ROOT/'figures'/('Figure_1_retention_v1.1.0_rc1.'+ext),dpi=400)
plt.close(fig)
fig,ax=plt.subplots(figsize=(7.15,5.25));fig.subplots_adjust(left=.15,right=.98,bottom=.17,top=.89)
x=[float(r['delta_ddg_A_to_B0']) for r in pairs];y=[float(r['delta_ddg_B0_to_Bomega']) for r in pairs]
ax.scatter(x,y,s=27,c='#28798E',alpha=.72,edgecolors='white',linewidths=.35,zorder=4)
ax.set_xlim(-.64,.46);ax.set_ylim(-.55,.48)
for v in [-.1,.1]:ax.axvline(v,color='#B56537',linestyle=(0,(2,3)),lw=1,zorder=1);ax.axhline(v,color='#B56537',linestyle=(0,(2,3)),lw=1,zorder=1)
ax.axhline(0,color='#61717E',lw=.8);ax.axvline(0,color='#61717E',lw=.8)
ax.set_xlabel(r'$\Delta\Delta G_{B_0}-\Delta\Delta G_A$ (kcal/mol)')
ax.set_ylabel(r'$\Delta\Delta G_{B_\omega}-\Delta\Delta G_{B_0}$ (kcal/mol)')
for xx,yy,label,ha in [(.43,.45,'Same stage signs','right'),(-.60,.45,'Opposite stage signs','left'),(-.60,-.51,'Same stage signs','left'),(.43,-.51,'Opposite stage signs','right')]:ax.text(xx,yy,label,ha=ha,va='center',fontsize=8.7,color='#687781')
fig.text(.15,.96,'112 matched pairs | signed operational stability changes',fontsize=11,weight='bold')
fig.text(.15,.055,'Dotted guides: descriptive +/-0.1 kcal/mol; no significance boundary.',fontsize=9,color='#835135')
for ext in ['png','pdf','svg']:fig.savefig(ROOT/'figures'/('Figure_2_signed_shifts_v1.1.0_rc1.'+ext),dpi=400)
plt.close(fig)
