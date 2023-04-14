package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.WorkDTO;
import ru.gamebot.backend.models.Work;
import ru.gamebot.backend.repository.WorkRepository;
import ru.gamebot.backend.util.WorkAlreadyExistException;
import ru.gamebot.backend.util.WorkMapper;
import ru.gamebot.backend.util.WorkNotFoundException;

import java.util.ArrayList;
import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class WorkService {

    private final WorkMapper workMapper;

    private final WorkRepository workRepository;

    public List<WorkDTO> getWorkList(){
        var works = workRepository.findAll();
        var worksDTO = new ArrayList<WorkDTO>();
        for(Work work: works){
            worksDTO.add(workMapper.workToWorkDTO(work));
        }
        return worksDTO;
    }

    @Transactional
    public void createWork(WorkDTO workDTO) throws WorkAlreadyExistException {
        var work = workMapper.workDTOToWork(workDTO);
        var existWork = workRepository.findByName(work.getName());
        if(existWork!=null){
            throw new WorkAlreadyExistException();
        }
        workRepository.save(work);
    }
    @Transactional
    public void deleteWork(Integer id){
        var work = workRepository.findById(id).orElseThrow(WorkNotFoundException::new);
        workRepository.delete(work);
    }
}