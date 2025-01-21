class Tournament():
    def __init__(self,**kwargs):
        print(kwargs.get("total_points"))
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.capacity = kwargs.get("capacity")
        self.total_points = kwargs.get("total_points") 
        self.organizer_id = kwargs.get("organizer_id")
        self.status = kwargs.get("status")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
    
    def __repr__(self):
        print(f'<Tournament {self.name} >')  