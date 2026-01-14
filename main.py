# main.py
import sys
from interview_simulator.workflows.graph import create_graph

# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_resume.pdf>")
        sys.exit(1)

    resume_path = sys.argv[1]
    # Get Job Description from user
    print("\nPaste the full Job Description below:")
    print("(When finished, press Ctrl+D on Mac/Linux or Ctrl+Z + Enter on Windows)\n")

    jd_lines = []
    try:
        while True:
            line = input()
            jd_lines.append(line)
    except EOFError:
        pass

    jd_text = "\n".join(jd_lines).strip()

    if not jd_text:
        print("Error: No job description provided.")
        sys.exit(1)

    app = create_graph()

    config = {"configurable": {"thread_id": "local_session_1"}}

    inputs = {
        "resume_path": resume_path,
        "jd_text": jd_text,
        "current_question_num": 0,
        "max_questions": 5,
        "interview_history": []
    }

    print("\n" + "="*60)
    print("STARTING AI INTERVIEW SIMULATOR")
    print("="*60)
    print("Analyzing resume and JD...\n")

    profile_printed = False  

    for step in app.stream(inputs, config, stream_mode="values"):
        print(f"DEBUG - Step keys: {list(step.keys())}")
        print(f"DEBUG - Current question num: {step.get('current_question_num', '?')}")
        print(f"DEBUG - Interview done? {step.get('interview_done', False)}\n")
    # Print profile ONLY ONCE
        if not profile_printed and "profile" in step and step["profile"]:
            print("\nCANDIDATE PROFILE")
            print("-" * 50)
            print(step["profile"].model_dump_json(indent=2))
            print("\nStarting interview...\n")
            profile_printed = True

    # Final evaluation - only once at the end
        if "evaluation" in step and step.get("evaluation"):
            eval_result = step["evaluation"]

            print("\n" + "="*70)
            print("FINAL EVALUATION RESULTS")
            print("="*70)

            # Summary (only once, nicely formatted)
            print(f"Overall Performance: {eval_result.overall_score:.1f}/10")
            print(f"Summary: {eval_result.summary}")
            print()

        # Per-question breakdown with clean formatting
            for i, q_eval in enumerate(eval_result.evaluations, 1):
                print("-" * 60)
                if q_eval.strengths:
                    print("Strengths:")
                    for s in q_eval.strengths:
                        print(f"  • {s}")
                if q_eval.weaknesses:
                    print("Areas to Improve:")
                    for w in q_eval.weaknesses:
                        print(f"  • {w}")
                if q_eval.feedback:
                    print("Feedback:")
                    print(f"  {q_eval.feedback}")
            print()  

            print("="*70)
            print("Interview completed successfully!")
            break
if __name__ == "__main__":
    main()