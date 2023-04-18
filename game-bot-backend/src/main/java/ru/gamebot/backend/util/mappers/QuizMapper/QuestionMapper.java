package ru.gamebot.backend.util.mappers.QuizMapper;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import ru.gamebot.backend.dto.QuestionDTO;
import ru.gamebot.backend.models.Question;

@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR
)
public interface QuestionMapper {
    Question questionDTOToQuestion(QuestionDTO questionDTO);

    QuestionDTO questionToQuestionDTO(Question question);
}
