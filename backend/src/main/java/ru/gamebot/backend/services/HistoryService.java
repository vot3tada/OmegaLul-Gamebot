package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.HistoryDTO;
import ru.gamebot.backend.models.HistoryPK;
import ru.gamebot.backend.repository.HistoryRepository;
import ru.gamebot.backend.util.exceptions.HistoryExceptions.HistoryNotExistsException;
import ru.gamebot.backend.util.exceptions.HistoryExceptions.HistoryNotFoundException;
import ru.gamebot.backend.util.mappers.HistoryMapper;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class HistoryService {
    private final HistoryRepository historyRepository;
    private final HistoryMapper historyMapper;

    public HistoryDTO getHistory(Integer chatId, Integer userId){
        var history = historyRepository.findById(new HistoryPK(userId, chatId)).orElseThrow(HistoryNotFoundException::new);
        return historyMapper.historyToHistoryDTO(history);
    }

    @Transactional
    public void updateHistory(HistoryDTO historyDTO) throws HistoryNotExistsException{
        var history = historyMapper.historyDTOToHistory(historyDTO);
        if(historyRepository.existsById(history.getHistoryPK())){
            historyRepository.save(history);
        }else {
            throw new HistoryNotExistsException("Attempt to add a new history: First of all add a person!");
        }
    }
}
