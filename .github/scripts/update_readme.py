import os
from collections import defaultdict
import math
import requests
import re

def get_problem_info(file_path):
    """파일명에서 문제 번호를 추출하고 solved.ac API를 통해 문제 정보를 가져옴"""
    file_name = os.path.basename(file_path)
    match = re.match(r'Prob(\d+)\.java', file_name)
    if not match:
        print(f"파일명이 형식에 맞지 않음: {file_name}")
        return None

    problem_number = match.group(1)
    print(f"문제 번호 추출: {problem_number}")

    try:
        print(f"solved.ac API 호출 시도: {problem_number}")
        response = requests.get(f'https://solved.ac/api/v3/problem/show', params={'problemId': problem_number})
        print(f"API 응답 상태: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"API 응답 데이터: {data}")
            return {
                'number': problem_number,
                'title': data.get('titleKo', '제목 없음'),
                'level': data.get('level', 0),
                'tags': [tag['displayNames'][0]['name'] for tag in data.get('tags', []) if tag['displayNames']],
                'link': f'https://www.acmicpc.net/problem/{problem_number}'
            }
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")

    print(f"기본 정보로 fallback: {problem_number}")
    return {
        'number': problem_number,
        'title': f'Problem {problem_number}',
        'level': 0,
        'tags': [],
        'link': f'https://www.acmicpc.net/problem/{problem_number}'
    }

def create_pie_chart(counts):
    """문제 난이도별 개수를 시각화하는 원형 차트 SVG 생성"""
    total = sum(counts.values())
    if total == 0:
        return '<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><text x="50" y="100">아직 풀은 문제가 없습니다</text></svg>'

    colors = {
        'bronze': '#CD7F32',
        'silver': '#C0C0C0',
        'gold': '#FFD700',
        'platinum': '#E5E4E2',
        'diamond': '#B9F2FF'
    }

    radius = 100
    center_x = 100
    center_y = 100
    paths = []
    current_angle = 0

    for diff, count in counts.items():
        if count == 0:
            continue

        percentage = count / total
        end_angle = current_angle + (percentage * 2 * math.pi)

        start_x = center_x + radius * math.cos(current_angle)
        start_y = center_y + radius * math.sin(current_angle)
        end_x = center_x + radius * math.cos(end_angle)
        end_y = center_y + radius * math.sin(end_angle)

        large_arc = 1 if percentage > 0.5 else 0
        path = f'<path d="M{center_x},{center_y} L{start_x},{start_y} A{radius},{radius} 0 {large_arc},1 {end_x},{end_y} Z" fill="{colors[diff]}" />'
        paths.append(path)

        text_angle = current_angle + (percentage * math.pi)
        text_x = center_x + (radius * 0.7) * math.cos(text_angle)
        text_y = center_y + (radius * 0.7) * math.sin(text_angle)
        percentage_text = f'{(percentage * 100):.1f}%'
        paths.append(f'<text x="{text_x}" y="{text_y}" text-anchor="middle" fill="white">{count} ({percentage_text})</text>')

        current_angle = end_angle

    legend_items = []
    y_offset = 220
    for i, (diff, color) in enumerate(colors.items()):
        if counts[diff] > 0:
            x_position = 40 + (i * 80)
            legend_items.extend([
                f'<rect x="{x_position}" y="{y_offset}" width="15" height="15" fill="{color}"/>',
                f'<text x="{x_position + 20}" y="{y_offset + 12}" font-size="12">{diff.capitalize()}</text>'
            ])

    svg = f'''<svg width="400" height="250" xmlns="http://www.w3.org/2000/svg">
        <circle cx="{center_x}" cy="{center_y}" r="{radius}" fill="#f0f0f0"/>
        {''.join(paths)}
        {''.join(legend_items)}
    </svg>'''

    return svg

def format_problems_table(problems_dict):
    """문제 목록을 마크다운 테이블 형식으로 포맷팅"""
    if not problems_dict:
        return "아직 풀은 문제가 없습니다."

    result = "\n| 문제 번호 | 제목 | 유형 | 태그 |\n|:---:|:---:|:---:|:---:|\n"
    all_problems = []

    for problem_type, problems in problems_dict.items():
        for problem_path in problems:
            info = get_problem_info(problem_path)
            if info:
                info['type'] = problem_type
                all_problems.append(info)

    all_problems.sort(key=lambda x: int(x['number']))

    for prob in all_problems:
        tags = ' '.join(f'`{tag}`' for tag in prob['tags'][:3])
        result += f"| [{prob['number']}]({prob['link']}) | {prob['title']} | {prob['type']} | {tags} |\n"

    return result

def get_problems_by_difficulty():
    """소스 코드 디렉토리에서 난이도별 문제 목록과 개수를 수집"""
    difficulties = ['bronze', 'silver', 'gold', 'platinum', 'diamond']
    problem_counts = defaultdict(int)
    problems_by_diff = defaultdict(lambda: defaultdict(list))

    base_path = 'src/main/java/org/example'
    print(f"기본 경로 탐색: {base_path}")

    for diff in difficulties:
        diff_path = os.path.join(base_path, diff)
        print(f"난이도 경로 확인: {diff_path}")
        if not os.path.exists(diff_path):
            print(f"경로 없음: {diff_path}")
            continue

        print(f"난이도 디렉토리 발견: {diff}")
        for problem_type in os.listdir(diff_path):
            type_path = os.path.join(diff_path, problem_type)
            print(f"유형 경로 확인: {type_path}")
            if os.path.isdir(type_path):
                for file in os.listdir(type_path):
                    print(f"파일 확인: {file}")
                    if file.endswith('.java') and file.startswith('Prob'):
                        print(f"문제 파일 발견: {file}")
                        problem_counts[diff] += 1
                        problems_by_diff[diff][problem_type].append(os.path.join(type_path, file))

    print(f"최종 문제 수: {dict(problem_counts)}")
    print(f"최종 문제 목록: {dict(problems_by_diff)}")
    return problems_by_diff, problem_counts

def create_readme_content(problems_by_diff, counts):
    """README 내용 생성"""
    pie_chart = create_pie_chart(counts)

    content = f"""# 알고리즘 문제 풀이

## 진행 상황
{pie_chart}

## 📊 해결한 문제 수
- 총 문제 수: {sum(counts.values())}
- 🥉 브론즈: {counts['bronze']}
- 🥈 실버: {counts['silver']}
- 🥇 골드: {counts['gold']}
- 💎 플래티넘: {counts['platinum']}
- 💫 다이아몬드: {counts['diamond']}

## 🥉 브론즈
{format_problems_table(problems_by_diff['bronze'])}

## 🥈 실버
{format_problems_table(problems_by_diff['silver'])}

## 🥇 골드
{format_problems_table(problems_by_diff['gold'])}

## 💎 플래티넘
{format_problems_table(problems_by_diff['platinum'])}

## 💫 다이아몬드
{format_problems_table(problems_by_diff['diamond'])}
"""
    print(f"생성된 README 내용 미리보기:\n{content[:200]}...")
    return content

def update_readme():
    """README.md 파일 업데이트"""
    try:
        problems_by_diff, counts = get_problems_by_difficulty()
        content = create_readme_content(problems_by_diff, counts)

        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print("README.md 업데이트 완료")

    except Exception as e:
        print(f"README 업데이트 중 오류 발생: {e}")
        raise

if __name__ == '__main__':
    update_readme()