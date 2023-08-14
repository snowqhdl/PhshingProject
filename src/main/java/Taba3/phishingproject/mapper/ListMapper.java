package Taba3.phishingproject.mapper;

import Taba3.phishingproject.dto.PredictedListDto;
import Taba3.phishingproject.entity.PredictedList;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface ListMapper {

    PredictedListDto.Response predictedListToResponse (PredictedList predictedList);
}
