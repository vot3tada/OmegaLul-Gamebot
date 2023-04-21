package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.BossDTO;
import ru.gamebot.backend.repository.BossRepository;
import ru.gamebot.backend.util.exceptions.BossExceptions.BossNotFoundException;
import ru.gamebot.backend.util.mappers.BossMapper.BossMapper;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class BossService {

    private final BossRepository bossRepository;
    private final BossMapper bossMapper;

    public BossDTO getBossById(Integer id){
        return bossMapper.bossToBossDTO(bossRepository.findById(id).orElseThrow(BossNotFoundException::new));
    }

    public List<BossDTO> getALlBoss(){
        return bossRepository.findAll().stream().map(bossMapper::bossToBossDTO).toList();
    }
}
