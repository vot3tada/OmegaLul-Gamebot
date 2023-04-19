package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class GetAllQuizDTO {
    private Integer id;
    private String name;
    private String photo;
}
