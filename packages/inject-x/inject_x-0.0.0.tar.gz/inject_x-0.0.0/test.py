from src.injectx import Injector, Presentation, Repository

inj: Injector = Injector().register_all_from_folder("test_case")

res_pres = inj.get_all_by_type(Presentation)
print(">>> res_pres:", res_pres)

res_repo = inj.get_all_by_type(Repository)
print(">>> res_repo:", res_repo)
