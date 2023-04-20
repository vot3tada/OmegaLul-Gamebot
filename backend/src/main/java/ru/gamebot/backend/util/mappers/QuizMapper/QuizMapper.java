package ru.gamebot.backend.util.mappers.QuizMapper;

import org.mapstruct.*;
import ru.gamebot.backend.dto.GetAllQuizDTO;
import ru.gamebot.backend.dto.QuestionDTO;
import ru.gamebot.backend.dto.QuizDTO;
import ru.gamebot.backend.models.Question;
import ru.gamebot.backend.models.Quiz;

@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR
)
public interface QuizMapper {
    @Mapping(target = "quizId", expression = "java(question.getQuiz().getId())")
    QuestionDTO toQuestionDto(Question question);
    @Mapping(target = "questions", ignore = true)
    Quiz quizDTOToQuiz(QuizDTO quizDTO);
    @Mapping(target = "questions", expression = "java(quiz.getQuestions().stream().map(x -> toQuestionDto(x)).toList())")
    QuizDTO quizToQuizDTO(Quiz quiz);
    GetAllQuizDTO quizToAllQuizDTO(Quiz quiz);
}
