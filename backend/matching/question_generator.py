def generate_interview_questions(recommendations):
    questions = []

    for rec in recommendations:
        skill = rec.get("skill")
        category = rec.get("category")

        if category == "programming_languages":
            questions.append(
                f"Write a small program using {skill} to demonstrate OOP principles."
            )
            questions.append(
                f"What are the performance considerations when using {skill}?"
            )

        elif category == "frameworks":
            questions.append(
                f"Explain the architecture of a typical application built with {skill}."
            )
            questions.append(
                f"How would you structure a scalable project using {skill}?"
            )

        elif category == "web_technologies":
            questions.append(
                f"How does {skill} improve front-end performance?"
            )
            questions.append(
                f"Explain real-world challenges when working with {skill}."
            )

        elif category == "databases":
            questions.append(
                f"Design a database schema using {skill} for an e-commerce system."
            )
            questions.append(
                f"What are indexing strategies in {skill}?"
            )

        elif category == "tools":
            questions.append(
                f"How would you integrate {skill} into a CI/CD pipeline?"
            )
            questions.append(
                f"What are common mistakes developers make when using {skill}?"
            )

        elif category == "concepts":
            questions.append(
                f"Explain {skill} with a real-world system design example."
            )
            questions.append(
                f"What problems does {skill} solve in modern software architecture?"
            )

    return questions[:10]