package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import ru.gamebot.backend.dto.GetGitlabDTO;
import ru.gamebot.backend.services.GitlabService;

import java.util.List;

@RestController
@RequestMapping("/api/gitlab")
@RequiredArgsConstructor
@Slf4j
public class GitLabContributionsController {
    private final GitlabService gitlabService;
    @GetMapping("/get/stats/{chatId}")
    public List<GetGitlabDTO> getStatsInChat(@PathVariable("chatId") Integer chatId){
        return gitlabService.getUsersStats(chatId);
    }

}
