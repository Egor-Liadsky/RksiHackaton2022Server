
import swagger

event_step = swagger.api.namespace(name='steps', path='/api/v1/event/')
event_step.description = "Методы событий на мероприятиях"