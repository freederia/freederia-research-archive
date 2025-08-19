import os
import re

# --- 설정 ---
# docs 폴더를 기준으로 작업합니다.
ROOT_DIR = "docs"

def prettify_title(filename):
    """파일이름을 예쁜 제목으로 바꿉니다. 예: AI-Driven_File.md -> AI Driven File"""
    name = os.path.splitext(filename)[0]
    # _와 -를 공백으로 바꾸고, 각 단어의 첫 글자를 대문자로 만듭니다.
    name = re.sub(r'[_\-]+', ' ', name).strip()
    return name.title()

def generate_index_files():
    """docs 폴더를 순회하며 index.md를 생성하고, 루트 인덱스도 만듭니다."""
    print("🚀 인덱스 파일 생성을 시작합니다...")
    
    # 각 날짜 폴더별로 생성된 인덱스 경로를 저장할 리스트
    created_folder_indices = []

    # 모든 하위 폴더를 탐색합니다.
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        # 현재 폴더에 .md 파일이 있는지 확인합니다. (index.md는 제외)
        md_files = [f for f in filenames if f.endswith('.md') and f != 'index.md']
        if not md_files:
            continue

        # --- 각 폴더의 index.md 생성 ---
        index_path = os.path.join(dirpath, "index.md")
        
        # 폴더 경로를 웹 URL 친화적으로 만듭니다 (예: docs/2025/08/06 -> /2025/08/06)
        permalink = "/" + os.path.relpath(dirpath, ROOT_DIR).replace("\\", "/")
        if permalink == "/.": # 루트 폴더의 경우
             permalink = "/"
        
        folder_title = os.path.basename(dirpath)

        lines = [
            "---",
            f"title: \"{folder_title} | 연구 문서 목록\"",
            "layout: default",
            f"permalink: {permalink}/", # 예: /2025/08/06/
            "---",
            f"# 📂 {folder_title} 연구 문서\n"
        ]

        md_files.sort() # 파일들을 가나다 순으로 정렬
        for md_file in md_files:
            title = prettify_title(md_file)
            # 링크에서 .md 확장자를 제거합니다. Jekyll이 알아서 .html로 연결해줍니다.
            link = os.path.splitext(md_file)[0]
            lines.append(f"- [{title}]({link})")
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"✅ 생성/업데이트 완료: {index_path}")
        
        # 루트 인덱스를 만들기 위해 폴더 정보를 저장합니다.
        # 최상위 docs 폴더는 제외합니다.
        if dirpath != ROOT_DIR:
            created_folder_indices.append(dirpath)

    # --- 루트 index.md 생성 ---
    if not created_folder_indices:
        print("ℹ️ 업데이트할 하위 폴더가 없습니다.")
        return

    root_index_path = os.path.join(ROOT_DIR, "index.md")
    lines = [
        "---",
        "title: \"Freederia Research Archive\"",
        "layout: default",
        "permalink: /", # 사이트의 메인 페이지가 되도록 설정
        "---",
        "# 📚 Freederia 전체 연구 아카이브\n",
        "날짜별로 정리된 연구 문서 목록입니다.\n"
    ]
    
    # 날짜 폴더를 최신순으로 정렬
    created_folder_indices.sort(reverse=True)
    
    for folder_path in created_folder_indices:
        # 웹 URL 경로로 변환
        relative_path = os.path.relpath(folder_path, ROOT_DIR).replace("\\", "/")
        lines.append(f"- [{relative_path}](/docs/{relative_path}/)")

    with open(root_index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ 루트 인덱스 생성/업데이트 완료: {root_index_path}")
    print("🎉 모든 작업이 완료되었습니다.")

if __name__ == "__main__":
    generate_index_files()