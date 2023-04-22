package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class GitLabUserDTO {
    private Long id;
    private String userName;
    private String name;
}
