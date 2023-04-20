package ru.gamebot.backend.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;
import java.util.List;

@Data
@NoArgsConstructor
public class GetEventDTO {
    private Integer id;
    private String name;
    @JsonFormat(pattern="yyyy-MM-dd HH:mm:ss")
    private java.util.Date startedAt;
    private List<PersonEventsDTO> members;

    public GetEventDTO(String name, Date startedAt, List<PersonEventsDTO> members, Integer id) {
        this.name = name;
        this.startedAt = startedAt;
        this.members = members;
        this.id = id;
    }
    public GetEventDTO(String name, Date startedAt, Integer id) {
        this.name = name;
        this.startedAt = startedAt;
        this.id = id;
    }


}
