import webview
import json
import os

SAVE_FILE = 'MochaVaultData.json'

class Api:
    def __init__(self):
        # 移除了那个害程序死循环的 window 绑定
        self.is_mini = False

    def save_data(self, data):
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            return False

    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []

    def toggle_mini(self):
        """控制系统窗口缩小和放大的真正核心！"""
        self.is_mini = not self.is_mini

        # 魔法修正：直接通过全局去找当前的一号窗口，绝不套娃！
        current_window = webview.windows[0]

        if self.is_mini:
            current_window.resize(190, 75)
        else:
            current_window.resize(550, 400)
        return self.is_mini


# 修复前缀 r，让 Python3.12 不再报小黄字警告
HTML_CONTENT = r"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>摩卡保险库</title>
    <style>
        :root {
            --mv-bg-deep: rgba(38, 24, 18, 1);
            --mv-bg-card: rgba(50, 32, 22, 1);
            --mv-bg-input: rgba(30, 18, 12, 1);
            --mv-gold: #e6be8a;
            --mv-gold-dim: #c49a6c;
            --mv-text: #f4dcb0;
            --mv-text-sub: #bcaaa4;
            --mv-border: rgba(180, 130, 80, 0.4);
            --mv-font: 'Microsoft YaHei', system-ui, sans-serif;
        }

        body, html { margin: 0; padding: 0; width: 100%; height: 100%; background: var(--mv-bg-deep); color: var(--mv-text); font-family: var(--mv-font); overflow: hidden; }

        #app-container { display: flex; flex-direction: column; height: 100vh; transition: opacity 0.2s; }
        #mini-container { display: none; height: 100vh; width: 100vw; background: linear-gradient(135deg, rgba(70,45,28,0.96), rgba(38,24,18,0.98)); align-items: center; justify-content: center; gap: 8px; color: var(--mv-gold); font-size: 16px; font-weight: bold; cursor: pointer; box-sizing: border-box; user-select: none; }
        #mini-container:hover { filter: brightness(1.2); text-shadow: 0 0 10px rgba(230,190,130,0.5); }
        .mini-icon { font-size: 20px; animation: float 2s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }

        body.is-mini #app-container { display: none; }
        body.is-mini #mini-container { display: flex; }

        .toolbar { padding: 12px 16px; background: rgba(50, 30, 18, 0.95); border-bottom: 1px solid var(--mv-border); display: flex; gap: 10px; align-items: center; position: relative; }
        button { padding: 8px 12px; border-radius: 6px; border: 1px solid var(--mv-border); background: rgba(180, 130, 80, 0.2); color: var(--mv-gold); cursor: pointer; font-weight: bold; transition: 0.2s; white-space: nowrap; }
        button:hover { filter: brightness(1.2); transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
        .search-box { flex: 1; padding: 8px 12px; border-radius: 6px; border: 1px solid var(--mv-border); background: var(--mv-bg-input); color: var(--mv-text); outline: none; }
        .search-box:focus { border-color: var(--mv-gold-dim); }

        .main-bd { display: flex; flex: 1; overflow: hidden; }
        .sidebar { width: 170px; border-right: 1px solid var(--mv-border); background: rgba(28, 16, 10, 0.8); overflow-y: auto; padding: 10px; }
        .note-item { padding: 10px 8px; border-radius: 6px; cursor: pointer; color: var(--mv-text-sub); margin-bottom: 5px; font-size: 13px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; transition: 0.2s; border: 1px solid transparent; }
        .note-item:hover { background: rgba(180, 130, 80, 0.15); }
        .note-item.active { background: rgba(230, 190, 130, 0.15); color: var(--mv-gold); border-color: rgba(180, 130, 80, 0.3); font-weight: bold; }

        .editor-area { flex: 1; display: flex; flex-direction: column; padding: 16px; gap: 12px; background: var(--mv-bg-deep); }
        .e-title { font-size: 16px; padding: 12px; border-radius: 8px; border: 1px solid var(--mv-border); background: var(--mv-bg-input); color: var(--mv-gold); font-weight: bold; outline: none; transition: 0.2s; }
        .e-title:focus { border-color: var(--mv-gold-dim); box-shadow: 0 0 5px rgba(230,190,130,0.3); }

        .e-content { flex: 1; font-size: 14px; padding: 14px; border-radius: 8px; border: 1px solid var(--mv-border); background: var(--mv-bg-input); color: var(--mv-text); resize: none; outline: none; line-height: 1.7; }
        .e-content:focus { border-color: var(--mv-gold-dim); box-shadow: 0 0 8px rgba(230,190,130,0.15); }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(180deg,#8d6e63,#5d4037); border-radius: 3px; }

        #status-msg { position: absolute; left: 50%; transform: translateX(-50%); background: rgba(45, 28, 20, 0.95); border: 1px solid var(--mv-border); padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.4); opacity: 0; transition: 0.3s; pointer-events: none; z-index: 100; top: -40px; }
        #status-msg.show { opacity: 1; top: 12px; }
    </style>
</head>
<body>
    <div id="mini-container" onclick="execToggleMini()">
        <span class="mini-icon">☕</span> 展开保险库
    </div>

    <div id="app-container">
        <div id="status-msg">✓ 提示</div>
        <div class="toolbar">
            <button onclick="newNote()">＋ 新建</button>
            <input type="text" class="search-box" id="searchInput" placeholder="🔍 搜索...">
            <button onclick="execToggleMini()" style="background: rgba(230, 190, 130, 0.15); color: #e6be8a; border-color: #c49a6c;">🎯 缩小折叠</button>
            <button onclick="copyContent()" style="background: rgba(100, 181, 246, 0.15); color: #64b5f6; border-color: rgba(100, 181, 246, 0.3);">📋 复制</button>
            <button onclick="deleteNote()" style="background: rgba(229, 115, 115, 0.15); color: #e57373; border-color: rgba(229, 115, 115, 0.3);">🗑️ 删除</button>
        </div>
        <div class="main-bd">
            <div class="sidebar" id="sidebar"></div>
            <div class="editor-area" id="editor" style="display: none;">
                <input type="text" class="e-title" id="noteTitle" placeholder="可以手动输入标题，粘贴内容也会自动覆盖...">
                <textarea class="e-content" id="noteContent" placeholder="粘贴带有 <Zilla> 的代码到这里吧！"></textarea>
            </div>
        </div>
    </div>

    <script>
        let notes = [];
        let currentId = null;
        let statusTimer = null;

        window.addEventListener('pywebviewready', function() {
            pywebview.api.load_data().then(function(data) {
                notes = data || [];
                renderList();
                if(notes.length > 0) openNote(notes[0].id);
            });
        });

        function execToggleMini() {
            pywebview.api.toggle_mini().then(function(isMini) {
                if (isMini) {
                    document.body.classList.add('is-mini');
                } else {
                    document.body.classList.remove('is-mini');
                }
            });
        }

        function showStatus(text, color = '#e6be8a') {
            const msg = document.getElementById('status-msg');
            msg.textContent = text; msg.style.color = color; msg.style.borderColor = color;
            msg.classList.add('show');
            clearTimeout(statusTimer);
            statusTimer = setTimeout(() => msg.classList.remove('show'), 2000);
        }

        function triggerSave(quiet = true) {
            pywebview.api.save_data(notes);
            renderList();
            if(!quiet) showStatus('✓ 已强制保存', '#81c784');
        }

        function newNote() {
            const id = Date.now().toString();
            notes.unshift({ id: id, title: '未命名笔记', content: '' });
            triggerSave(true);
            openNote(id);
        }

        function openNote(id) {
            currentId = id;
            const note = notes.find(n => n.id === id);
            if (!note) return;
            document.getElementById('editor').style.display = 'flex';
            document.getElementById('noteTitle').value = note.title || '未命名笔记';
            document.getElementById('noteContent').value = note.content || '';
        }

        function deleteNote() {
            if (!currentId) return;
            const note = notes.find(n => n.id === currentId);
            const titleName = note && note.title ? note.title : '这篇笔记';
            if (confirm(`☕ 摩卡保险库提示：\n\n确定要将【${titleName}】彻底删除吗？`)) {
                notes = notes.filter(n => n.id !== currentId);
                currentId = null;
                document.getElementById('editor').style.display = 'none';
                triggerSave(true);
                showStatus('🗑️ 笔记已删除', '#e57373');
                if(notes.length > 0) openNote(notes[0].id);
            }
        }

        function copyContent() {
            if (!currentId) return;
            const note = notes.find(n => n.id === currentId);
            const val = note.content || '';
            if (!val.trim()) { showStatus('笔记是空的哦！', '#e57373'); return; }
            const copyTa = document.createElement('textarea');
            copyTa.value = val; document.body.appendChild(copyTa);
            copyTa.select(); document.execCommand('copy'); document.body.removeChild(copyTa);
            showStatus('📋 笔记正文已全选并复制！', '#64b5f6');
        }

        function renderList() {
            const keyword = document.getElementById('searchInput').value.toLowerCase();
            const list = document.getElementById('sidebar');
            list.innerHTML = notes
                .filter(n => (n.title||'').toLowerCase().includes(keyword) || (n.content||'').toLowerCase().includes(keyword))
                .map(n => `<div class="note-item ${n.id === currentId ? 'active' : ''}" onclick="openNote('${n.id}')">🔖 ${(n.title||'未命名笔记').replace(/</g, "&lt;")}</div>`)
                .join('');
        }

        function refreshTitleExtract(contentStr, noteObj) {
            const match = contentStr.match(/【([^】]+)】/);
            if (match && match[1]) {
                const extracted = match[1].replace(/小剧场\./g, '').trim();
                if (extracted) {
                    noteObj.title = extracted;
                    document.getElementById('noteTitle').value = extracted;
                }
            }
        }

        document.getElementById('noteContent').addEventListener('input', function() {
            if (currentId) {
                const note = notes.find(n => n.id === currentId);
                note.content = this.value;
                refreshTitleExtract(this.value, note);
                triggerSave(true);
            }
        });

        document.getElementById('noteTitle').addEventListener('input', function() {
            if (currentId) {
                const note = notes.find(n => n.id === currentId);
                note.title = this.value;
                triggerSave(true);
            }
        });

        document.getElementById('searchInput').addEventListener('input', renderList);

        document.addEventListener('keydown', e => {
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault(); triggerSave(false);
            }
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    api_bridge = Api()

    # 【修复重点】：直接生成窗口，不再绑定到 api_bridge 里啦！
    window = webview.create_window(
        title='☕ 摩卡保险库',
        html=HTML_CONTENT,
        js_api=api_bridge,
        width=850,
        height=600,
        min_size=(180, 50),
        background_color='#1c120a'
    )

    webview.start()