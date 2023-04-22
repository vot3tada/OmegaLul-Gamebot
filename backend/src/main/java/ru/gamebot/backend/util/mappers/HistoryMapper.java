package ru.gamebot.backend.util.mappers;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import ru.gamebot.backend.dto.HistoryDTO;
import ru.gamebot.backend.models.History;

@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR
)
public interface HistoryMapper {
    @Mapping(target = "historyPK", expression = "java(historyDTO.toHistoryPK())")
    History historyDTOToHistory(HistoryDTO historyDTO);
    @Mapping(target = "chatId", expression = "java(history.getHistoryPK().getPersonChatId())")
    @Mapping(target = "userId", expression = "java(history.getHistoryPK().getPersonUserId())")
    HistoryDTO historyToHistoryDTO(History history);

}
