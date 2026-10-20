"""Build the original synthetic demos from the current development components."""
from pathlib import Path
import sys,re,json,subprocess
from html import escape
ROOT=Path(__file__).resolve().parents[1];SKILL=ROOT/'skills/paper-to-html-v2.4'
sys.path.insert(0,str(SKILL/'scripts'))
from teaching_contract import render_teaching

for en in (False,True):
    folder=ROOT/'demo'/('en' if en else '');p=folder/'content.html';s=p.read_text('utf8')
    for key in ('overview','a','b'):
        target=('en-' if en else 'demo-')+key+'-text'
        opening=re.search(r'<div\b[^>]*id="'+target+r'"[^>]*>',s);assert opening
        start=opening.end();depth=1;end=None
        for tag in re.finditer(r'<div\b[^>]*>|</div>',s[start:]):
            depth+=-1 if tag.group().startswith('</') else 1
            if depth==0:end=start+tag.start();break
        old=s[start:end];oldids=re.findall(r'id="([^"]+)"',old)
        a,b=(55,38) if key=='b' else (60,35)
        if en:
            data={'question':['Compare groups A and B on one measurement scale. Each bar is a group summary; these invented values demonstrate the interface, not a biological experiment.'],
                  'legend':[{'visual':'Orange bar / blue bar','meaning':'Group A / group B, respectively.'},{'visual':'Bar height and number above it','meaning':'The invented measurement value, in arbitrary demonstration units; not a sample count or uncertainty estimate.'}],
                  'reasoning':[f'Group A is {a} and B is {b}, so the observed summary for A is {a-b} units higher. The same scale permits this descriptive comparison.', 'No replicate distribution or uncertainty is supplied. The figure therefore cannot establish a stable population difference or a causal mechanism.'],
                  'next_question':'Next ask whether the difference repeats, then design a comparison that distinguishes possible causes. The second synthetic panel illustrates another observation; it is not an independent real-world validation.'}
            caption='<h3>Read the comparison, then ask what it supports</h3><p>Original synthetic chart. Group values are invented for interface demonstration; no real paper is reproduced.</p>'
        else:
            data={'question':['用同一测量尺度比较 A、B 两组。每根柱是一个组的汇总值，数值为界面演示编写，不对应真实实验。先读出谁高，再问这个比较能支持什么。'],
                  'legend':[{'visual':'橙色柱／蓝色柱','meaning':'分别对应 A 组／B 组。'},{'visual':'柱高及柱上数字','meaning':'模拟测量值，单位为演示用任意单位；不是样本量，也不表示误差范围。'}],
                  'reasoning':[f'A 为 {a}，B 为 {b}，A 的汇总值比 B 高 {a-b} 个演示单位。同一尺度允许我们作这个描述性比较。','图中没有重复样本分布和不确定性范围，因此不能仅凭两柱判断差异是否稳定，更不能把差异直接解释成因果机制。'],
                  'next_question':'下一问是差异能否重复、可能由什么引起；需要重复测量及能区分原因的比较设计。另一模拟面板仅展示另一次观察，不是真实研究的独立验证。'}
            caption='<h3>先读出比较，再判断它能说明什么</h3><h4>演示图注</h4><p>Original synthetic chart. Group values are invented for interface demonstration; no real paper is reproduced.</p><h4>完整翻译</h4><p>原创模拟图：组别数值为界面演示编写，不复现真实论文结果。</p>'
        new=caption+render_teaching(data,('en' if en else 'zh')+'-teaching-'+key)
        # Keep public lookup anchors from the previous synthetic demo.
        newids=set(re.findall(r'id="([^"]+)"',new))
        new=''.join('<span id="'+escape(i)+'"></span>' for i in oldids if i not in newids)+new
        s=s[:start]+new+s[end:]
    # Overview is itself a detailed demonstration unit.
    s=re.sub(r'data-reader-panel="overview"', 'data-reader-panel="overview" data-reader-teaching-mode="detailed"',s)
    # Make generation idempotent.
    s=s.replace(' data-reader-teaching-mode="detailed" data-reader-teaching-mode="detailed"',' data-reader-teaching-mode="detailed"')
    p.write_text(s,encoding='utf8')
    manifest={'domain':'nonbiology','legend':[{'id':'method','label':'Comparison' if en else '比较方法','color':'#ffedc5'}],'concepts':[]}
    manifest_path=folder/'concepts.json';manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    subprocess.run([sys.executable,str(SKILL/'scripts/build_reader.py'),'--content',str(p),'--paper-id','original-demo-en-v24' if en else 'original-demo-zh-v24','--concepts',str(manifest_path),'--out',str(folder/'paper-reading.html')],check=True)
    output=folder/'paper-reading.html';html=output.read_text('utf8').replace('<title>论文共读组件</title>','<title>paper-to-html · '+('Original interactive demo' if en else '原创交互演示')+'</title>')
    if en:
        translations={'带着当前问题读图':'Question and design','本图图例与元素':'Legend and plotted elements','从实际结果读到判断':'From observation to inference','结论边界与后续联系':'Limits and next question','图中位置／元素':'Visual element','含义与读法':'Meaning',
        '随手记 · 随手问':'Notes and questions','问题保存到当前论文项目，下轮共读时处理。':'Save to the local paper project for a later assistant session.','想到什么就写什么，可粘贴截图':'Keep a question; screenshots can be pasted.','存下这条 · 下轮处理':'Save for a later session','我有疑问':'Question','补充内容':'Addition','修改要求':'Change request','记录类型':'Note type','放在哪一块':'Section','问题或要求':'Question or request','添加截图附件':'Attach screenshot','清除截图':'Clear attachments','退出编辑':'Exit editing','刷新记录':'Refresh notes','随手记':'Notes',
        '回到刚才阅读处':'Return to reading','展开荧光笔':'Open highlighter','术语彩色：开启':'Term colors: on','术语彩色：关闭':'Term colors: off','一键展开':'Expand all','一键收起':'Collapse all','撤销':'Undo','开启':'Enable','关闭':'Close','图例':'Legend','复位':'Reset','放大图片':'Zoom in','缩小图片':'Zoom out','论文图片预览':'Figure preview','当前放大图':'Zoomed figure','放大查看：':'Zoom: ',
        '基础 · 文章内容':'Article','知识区':'Knowledge','进阶内容':'Advanced','进阶知识区':'Assessment','读者总结与评议':'Reader assessment','工作稿 · 尚未正式编号':'Original demo · v2.4 components','版本设置':'Version settings','保留网站历史版本吗？':'Keep reader history?','保存方式':'Retention','请选择':'Choose','保存选择':'Save choice','稍后选择':'Later','项目版本设置':'Reader version settings','此文件是离线快照，备份方式以项目设置为准。':'This is an offline snapshot; retention belongs to the local project.','导出时的设置：':'Snapshot retention: ','尚未选择':'Not configured','请让助手在项目中配置备份方式；此文件不单独保存设置。':'Configure retention in the local project; this snapshot does not save settings.','文件预览不能保存提问':'File preview cannot save project notes','请通过当前项目阅读服务打开':'Open the local project service','已连接项目提问队列，下轮共读时读取处理。':'Connected to the local project queue for a later session.','已存入当前论文项目，下轮共读时助手读取；不会自动即时回复。':'Saved to the local paper project for a later session; no instant response.'}
        for a,b in sorted(translations.items(),key=lambda x:-len(x[0])):html=html.replace(a,b)
        html=html.replace('lang="zh-CN"','lang="en"',1)
    output.write_text(html,encoding='utf8')
print('Both original demos rebuilt with current teaching, legend and interaction components.')
