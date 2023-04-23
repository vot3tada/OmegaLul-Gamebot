package ru.gamebot.backend.util.mappers;

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

}
